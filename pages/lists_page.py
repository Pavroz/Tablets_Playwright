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

    def create_participant(self, middlename=None, subject=None, position=None, image=None):
        """Создание участника с генерацией значений"""
        with allure.step('Открытие модального окна создания участника'):
            self.page.locator(loc.create_button).click()
            lastname_field = self.page.locator(loc.lastname_field)
            firstname_field = self.page.locator(loc.firstname_field)
        # Генерирация строковых значений
        with allure.step('Генерация случайных значений'):
            generated_lastname = self.generate_random()
            generated_firstname = self.generate_random()
        # Ввод строковых значений
        with allure.step('Заполнение обязательных полей ввода'):
            lastname_field.fill(generated_lastname)
            firstname_field.fill(generated_firstname)
        with allure.step('Заполнение поля ввода "Отчество"'):
            if middlename:
                middlename_field = self.page.locator(loc.middlename_field)
                generated_middlename = self.generate_random()
                middlename_field.fill(generated_middlename)
        with allure.step('Заполнение поля ввода "Субъект"'):
            if subject:
                subject_field = self.page.locator(loc.subject_field)
                generated_subject = self.generate_random()
                subject_field.fill(generated_subject)
        with allure.step('Заполнение поля ввода "Должность"'):
            if position:
                position_field = self.page.locator(loc.position_field)
                generated_position = self.generate_random()
                position_field.fill(generated_position)
        with allure.step('Добавление изображения'):
            if image:
                self.page.set_input_files(loc.add_image_button, loc.file_path)

        with allure.step('Подтверждение создания'):
            self.page.locator(loc.create_button_in_modal).click()
        new_lastname = self.page.locator(f'//*[text()="{generated_lastname}"]')
        with allure.step('Проверка созданного участника с сгенерированным именем'):
            expect(new_lastname).to_have_text(generated_lastname)
        return new_lastname.inner_text()



    def update_participant(self, lastname):
        """Поиск участника по имени, очистка полей и генерация новых значений"""
        with allure.step('Поиск созданного участника и нажатие на него'):
            line_to_participant = self.page.locator(f'//*[text()="{lastname}"]')
            line_to_participant.click()
        with allure.step('Открытие модального окна редактирования участника'):
            self.page.locator(loc.edit_button).click()
            lastname_field = self.page.locator(loc.lastname_field)
            firstname_field = self.page.locator(loc.firstname_field)
        with allure.step('Очистка полей ввода'):
            lastname_field.clear()
            firstname_field.clear()
        with allure.step('Генерация случайных значений'):
            generated_lastname = self.generate_random()
            generated_firstname = self.generate_random()
        with allure.step('Заполнение обязательных полей ввода'):
            lastname_field.fill(generated_lastname)
            firstname_field.fill(generated_firstname)
        with allure.step('Подтверждение создания'):
            self.page.locator(loc.save_button_in_modal).click()
        new_lastname = self.page.locator(f'//*[text()="{generated_lastname}"]')
        with allure.step('Проверка отредактированного участника с новым сгенерированным именем'):
            expect(new_lastname).to_have_text(generated_lastname)
        return new_lastname.inner_text()

    def delete_participant(self, lastname):
        """Поиск участника по имении удаление"""
        with allure.step('Поиск созданного участника и нажатие на него'):
            line_to_participant = self.page.locator(f'//*[text()="{lastname}"]')
            line_to_participant.click()
        with allure.step('Нажатие на кнопку удаления'):
            delete_button = self.page.locator(loc.delete_button)
            delete_button.click()
        with allure.step('Подтверждение удаления'):
            self.page.locator(loc.apply_delete_button).click()
        with allure.step('Проверка, что созданный ранее участник удален'):
            expect(line_to_participant).not_to_be_visible()
        return None

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


    def load_participant(self):
        """Загрузка участников из файла"""
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator(loc.load_button).click()
        file_chooser = fc_info.value
        file_chooser.set_files(loc.load_participant_file)

    def get_all_participant(self) -> List[Dict[str, str]]:
        """Возвращает список всех участников с данными"""
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

    def pagination_page(self):
        pagination = self.page.locator(loc.pagination_button).all()
        for page in pagination:
            page.click()

    # Проба реализации инкапсуляции через __ у метода
    def __switch_by_page(self, value: int):
        # Открываем dropdown
        self.page.locator(loc.dropdown_page_button).click()
        # Формируем селектор для нужного элемента
        item_locator = f'//div[text()="{value} / стр."]'
        # Дожидаемся, что элемент видим и стабильный
        self.page.locator(item_locator).first.wait_for(state="visible")
        self.page.locator(item_locator).first.click()

    def switch_by_10_page(self):
        self.__switch_by_page(10)

    def switch_by_20_page(self):
        self.__switch_by_page(20)

    def switch_by_50_page(self):
        self.__switch_by_page(50)

    def switch_by_100_page(self):
        self.__switch_by_page(100)