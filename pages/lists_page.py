import re
from typing import List, Dict

from pages.base_page import BasePage
from locators import lists_locators as loc
from playwright.sync_api import expect
from time import sleep
import allure
import random
import string

class ListsPage(BasePage):

    def __init__(self, page):
        super().__init__(page)


    @staticmethod
    def generate_random(prefix='Test_', length = 20):
        """Генерация случайного значения"""
        suffix = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(length))
        return f'{prefix}{suffix}'

    @allure.step('Создание участника с генерацией значений')
    def create_participant(self, middlename=None, subject=None, position=None, image=None) -> str:
        """Создание участника с генерацией значений"""
        self.page.locator(loc.create_button).click()
        lastname_field = self.page.locator(loc.lastname_field)
        firstname_field = self.page.locator(loc.firstname_field)
        # Генерирация строковых значений
        generated_lastname = self.generate_random()
        generated_firstname = self.generate_random()
        # Ввод строковых значений
        lastname_field.fill(generated_lastname)
        firstname_field.fill(generated_firstname)
        if middlename:
            middlename_field = self.page.locator(loc.middlename_field)
            generated_middlename = self.generate_random()
            middlename_field.fill(generated_middlename)
        if subject:
            subject_field = self.page.locator(loc.subject_field)
            generated_subject = self.generate_random()
            subject_field.fill(generated_subject)
        if position:
            position_field = self.page.locator(loc.position_field)
            generated_position = self.generate_random()
            position_field.fill(generated_position)
        if image:
            self.page.set_input_files(loc.add_image_button, loc.file_path)

        self.page.locator(loc.create_button_in_modal).click()
        new_lastname = self.page.locator(f'//*[text()="{generated_lastname}"]')
        expect(new_lastname).to_have_text(generated_lastname)
        return new_lastname.inner_text()


    @allure.step('Поиск участника по имени, очистка полей и генерация новых значений')
    def update_participant(self, lastname: str) -> str:
        """Поиск участника по имени, очистка полей и генерация новых значений"""
        line_to_participant = self.page.locator(f'//*[text()="{lastname}"]')
        line_to_participant.click()
        self.page.locator(loc.edit_button).click()
        lastname_field = self.page.locator(loc.lastname_field)
        firstname_field = self.page.locator(loc.firstname_field)
        lastname_field.clear()
        firstname_field.clear()
        generated_lastname = self.generate_random()
        generated_firstname = self.generate_random()
        lastname_field.fill(generated_lastname)
        firstname_field.fill(generated_firstname)
        self.page.locator(loc.save_button_in_modal).click()
        new_lastname = self.page.locator(f'//*[text()="{generated_lastname}"]')
        expect(new_lastname).to_have_text(generated_lastname)
        return new_lastname.inner_text()

    @allure.step('Поиск участника по имении удаление')
    def delete_participant(self, lastname: str):
        """Поиск участника по имении удаление"""
        line_to_participant = self.page.locator(f'//*[text()="{lastname}"]')
        line_to_participant.click()
        delete_button = self.page.locator(loc.delete_button)
        delete_button.click()
        self.page.locator(loc.apply_delete_button).click()
        expect(line_to_participant).not_to_be_visible()
        return None

    @allure.step('Просмотр добавленного изображения (три варианта)')
    def view_added_image(self, lastname):
        """Просмотр добавленного изображения (три варианта)"""
        line_to_participant = self.page.locator(f'//*[text()="{lastname}"]').first
        line_to_participant.click()
        self.page.locator(loc.view_image_button).click()
        modal = self.page.locator(loc.modal_with_image)
        no_image = self.page.locator(loc.no_image_notification)
        btn_disabled = self.page.locator(loc.button_is_disable)
        try:
            # Ждём модалку с картинкой
            modal.wait_for(state="visible", timeout=5000)
            expect(modal).to_be_visible()
            self.page.locator(loc.modal_close_button).click()
            return
        except:
            pass

        try:
            # Ждём уведомление об отсутствии изображения
            no_image.wait_for(state="visible", timeout=2000)
            expect(no_image).to_have_text('Для участника не загружено изображение!')
            return
        except:
            pass

        try:
            # Ждём заблокированную кнопку
            btn_disabled.wait_for(state="visible", timeout=2000)
            expect(btn_disabled).to_be_disabled()
            return
        except:
            pass

            # Если ничего не появилось
        raise Exception("Не найдено ни одно из ожидаемых состояний!")

    @allure.step('Загрузка участников из файла')
    def load_participant(self):
        """Загрузка участников из файла"""
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator(loc.load_button).click()
        file_chooser = fc_info.value
        file_chooser.set_files(loc.load_participant_file)
    @allure.step('Возвращение списка всех участников с данными')
    def get_all_participant(self) -> List[Dict[str, str]]:
        """Возвращение списка всех участников с данными"""
        participants = []
        rows = self.page.locator(loc.line_to_participant)
        rows.first.wait_for(state="visible")  # ждём хотя бы одну строку
        count = rows.count()

        for i in range(count):
            row = rows.nth(i)
            cells = row.locator("td")
            participant = {
                "last_name": cells.nth(0).inner_text().strip(),
                "first_name": cells.nth(1).inner_text().strip(),
                "middle_name": cells.nth(2).inner_text().strip(),
                "country": cells.nth(3).inner_text().strip(),
                "extra": cells.nth(4).inner_text().strip(),
                "status": cells.nth(5).inner_text().strip(),
            }
            participants.append(participant)
            print(f'\n{participant}')
        return participants

    @allure.step('Переключение страниц')
    def pagination_page(self):
        pagination = self.page.locator(loc.pagination_button).all()
        for page in pagination:
            page.click()
            # sleep(1)

    @allure.step('Переключение количества отображения данных')
    # Проба реализации инкапсуляции через __ у метода
    def switch_page(self, value: int):
        # Формируем селектор для нужного элемента
        item_locator = f'//div[text()="{value} / стр."]'
        # Открываем dropdown
        self.page.locator(loc.dropdown_page_button).click()
        # Дожидаемся, что элемент видим и стабильный
        self.page.locator(item_locator).first.wait_for(state="visible")
        self.page.locator(item_locator).first.click()

    # @allure.step('Переключение количества отображения данных')
    # def switch_page(self, value: int):
    #     self.__switch_page(value)

    @allure.step('Поиск участника по фамилии')
    def search_participant_by_lastname(self, lastname: str):
            search_field = self.page.locator(loc.search_field)
            search_field.wait_for(state="visible")
            search_field.fill(lastname)
            search_field.press('Enter')
            expect(self.page.locator(loc.selected_row)).to_be_visible()
            expect(self.page.locator(f'//td//span[text()="{lastname}"]')).to_be_visible()

class Sorting(BasePage):

    def __init__(self, page):
        super().__init__(page)

    @allure.step('Сортировка по каждому значению')
    def sort_up(self, value: str):
        self.page.locator(loc.sort_button).click()
        self.page.locator(loc.cleaning_button).click()

        if value == 'lastname':
            self.page.locator(loc.checkbox_lastname).click()
        if value == 'firstname':
            self.page.locator(loc.checkbox_firstname).click()
        if value == 'middlename':
            self.page.locator(loc.checkbox_middlename).click()
        if value == 'subject':
            self.page.locator(loc.checkbox_subject).click()
        if value == 'position':
            self.page.locator(loc.checkbox_position).click()
        if value == 'image':
            self.page.locator(loc.checkbox_image).click()

        self.page.locator(loc.sort_up).click()
        self.page.locator(loc.sorting_apply_button).click()