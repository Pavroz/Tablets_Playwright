from pages.base_page import BasePage
from locators import configuration_locators as loc
from playwright.sync_api import Page, expect
from time import sleep
import allure
import random
import string


class ConfigurationPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def generate_scheme_name(self, prefix='Scheme_', length=15):
        """Генерация имени для тестовой схемы"""
        suffix = ''.join(random.choice(string.ascii_lowercase + string.digits)
                         for _ in range(length - len(prefix)))
        return f'{prefix}{suffix}'

    def go_to_lists_page(self):
        """Переход на страницу списка участников"""
        self.page.locator(loc.lists_page).click()

    def create_scheme(self):
        """Создание схемы"""
        # name = "Scheme_" + str(random.randint(1000, 9999))
        name = self.generate_scheme_name()
        self.page.locator(loc.create_scheme_button).click()
        self.page.wait_for_selector('nz-modal-container')
        self.page.locator(loc.name_field).fill(name)
        # Ловим открытие file chooser
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role(
                'button',
                name='Загрузите схему зала в формате .svg (до 2 МБ)'
            ).click()
        # когда file chooser открыт — передаём файл
        file_chooser = fc_info.value
        file_chooser.set_files(loc.scheme_path)
        self.page.locator(loc.create_button).click()
        return name

    def choice_scheme(self, name_scheme):
        """Выбор схемы в дропдауне"""
        self.page.locator(loc.schemes_selector).click()
        self.page.locator(loc.schemes_dropdown).wait_for(state='visible')
        self.page.locator(loc.schemes_in_dropdown, has_text=name_scheme).click()

    def apply_scheme(self):
        """Применение схемы"""
        # Ждём, пока кнопка станет видимой и enabled
        button = self.page.locator(loc.apply_scheme_button, has_text='Применить')
        button.wait_for(state='visible')
        # button.wait_for(state="enabled")
        button.click()

    def edit_scheme(self, name_scheme):
        # new_name_scheme = "Scheme_" + str(random.randint(1000, 9999))
        new_name_scheme = self.generate_scheme_name()
        self.choice_scheme(name_scheme)
        self.page.locator(loc.edit_scheme_button).click()
        self.page.locator(loc.name_field_in_edit_scheme).fill(new_name_scheme)
        self.page.locator(loc.save_button_in_edit_scheme).click()

    def delete_scheme(self, name_scheme):
        """Выбор схемы в списке и удаление"""
        self.choice_scheme(name_scheme)
        # Удаление
        self.page.locator(loc.delete_scheme_button).click()
        self.page.wait_for_selector('nz-modal-confirm-container')
        self.page.locator(loc.yes_scheme_button).click()
        # Проверка, что схема удалилась
        self.page.locator(loc.schemes_selector).click()
        self.page.locator(loc.schemes_dropdown).wait_for(state='visible')
        # Проверка, что элемент не существует вообще
        expect(self.page.locator(loc.schemes_in_dropdown, has_text=name_scheme)).to_have_count(0)

    def copy_scheme(self, name_scheme):
        """Выбор схемы в списке и копирование"""
        new_name_scheme = self.generate_scheme_name()
        # Выбор схемы
        self.choice_scheme(name_scheme)
        # Копирование
        self.page.locator(loc.copy_scheme_button).click()
        self.page.wait_for_selector(loc.nz_modal_container)
        self.page.locator(loc.name_field_in_copy_scheme).fill(new_name_scheme)
        self.page.locator(loc.copy_button).click()
        # Проверка, что схема появилась в списке схем
        self.page.locator(loc.schemes_selector).click()
        self.page.locator(loc.schemes_dropdown).wait_for(state='visible')
        expect(self.page.locator(loc.schemes_in_dropdown, has_text=name_scheme)).to_be_visible()


    def load_new_scheme(self, name_scheme):
        """Выбор схемы в списке и загрузка новой схемы"""
        # Выбор схемы
        self.choice_scheme(name_scheme)
        # Ловим открытие file chooser
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator(loc.load_new_scheme_button).click()
        # когда file chooser открыт — передаём файл
        file_chooser = fc_info.value
        file_chooser.set_files(loc.new_scheme_path)
        # Проверка, что лоадер на кнопке пропал
        expect(self.page.locator(loc.loader_on_button)).not_to_be_visible()
        # self.page.locator(loc.loader_on_button).wait_for(state='detached')

    def download_scheme(self, name_scheme):
        """Выбор схемы в списке и скачивание"""
        self.choice_scheme(name_scheme)
        # Контекстный менеджер скаичвания файла
        with self.page.expect_download() as download_info:
            self.page.locator(loc.download_scheme_button).click()
        download = download_info.value
        # Проверяем, что расширение файла в конце .svg
        assert download.suggested_filename.lower().endswith('.svg')
        print(f'\ndownload.suggested_filename')
        print(download.url)
        print(download.page)


    def create_max_number_of_characters_scheme(self, quantity=256):
        """Создание схемы с максимальным количеством символов в названии"""
        # name = ''.join(random.choice(string.ascii_lowercase + string.digits)
        #                for _ in range(quantity))
        name = self.generate_scheme_name()
        self.page.locator(loc.create_scheme_button).click()
        self.page.wait_for_selector('nz-modal-container')
        self.page.locator(loc.name_field).fill(name)
        # Ловим открытие file chooser
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role(
                'button',
                name='Загрузите схему зала в формате .svg (до 2 МБ)'
            ).click()
        # когда file chooser открыт — передаём файл
        file_chooser = fc_info.value
        file_chooser.set_files(loc.scheme_path)
        expect(self.page.locator(loc.create_button)).to_be_disabled()
        self.page.locator(loc.cancel_button).click()
        return name

    def create_place(self, name_scheme):
        # Выбор схемы
        self.choice_scheme(name_scheme)
        self.page.locator(loc.edit_switch_off).click()

        add_button = self.page.locator(loc.add_place_on_scheme_button)
        add_button.wait_for(state="attached")
        add_button.wait_for(state="visible")
        expect(add_button).to_be_enabled()
        add_button.hover()
        add_button.click(force=True)

        scheme = self.page.locator(loc.scheme)
        scheme.wait_for(state="visible")  # безопаснее перед кликом
        # размеры схемы известны
        width = 800
        height = 443

        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        # клик в случайное место
        scheme.click(position={"x": x, "y": y})

        self.page.wait_for_selector(loc.nz_modal_container, state="visible")
        self.page.locator(loc.location_on_scheme).click()
        self.page.locator(loc.location_list_on_scheme).first.click()
        number = str(random.randint(0, 100))
        self.page.locator(loc.line_on_scheme).fill(number)
        self.page.locator(loc.place_on_scheme).fill(number)
        self.page.locator(loc.create_place_button).click()
