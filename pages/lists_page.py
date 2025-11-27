from pages.base_page import BasePage
from locators import lists_locators as loc
from playwright.sync_api import Page, expect
from time import sleep
import allure
import random
import string

class ListsPage(BasePage):

    def __init__(self, page):
        super().__init__(page)


    @staticmethod
    def generate_random(prefix='Test_', length = 20):
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
        line_to_participant =self.page.locator(f'//*[text()="{lastname}"]')
        line_to_participant.click()
        self.page.locator(loc.view_image_button).click()
        modal = self.page.locator(loc.modal_with_image)
        if modal.count() > 0:
            expect(modal).to_be_visible()
        elif self.page.locator(loc.no_image_notification).count() > 0:
            expect(self.page.locator(loc.no_image_notification)).to_have_text(
                'Для участника не загружено изображение!'
            )
        else:
            expect(self.page.locator(loc.button_is_disable)).to_be_disabled()

