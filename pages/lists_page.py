from selenium.common import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.locators import lists_locators as loc
from time import sleep
import allure
import random
import string

class ListsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    @staticmethod
    def generate_random(prefix='Test_', length = 20):
        suffix = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(length))
        return f'{prefix}{suffix}'

    def go_to_back(self):
        """Стрелка назад (выход в меню профилей)"""
        with allure.step('Переход к списку профилей'):
            self.got_to_back()

    def create_participant(self, middlename=None, subject=None, position=None, image=None):
        """Создание участника с генерацией значений"""
        with allure.step('Открытие модального окна создания участника'):
            self.wait_for_presence(loc.create_button).click()
            lastname_field = self.wait_for_presence(loc.lastname_field)
            firstname_field = self.wait_for_presence(loc.firstname_field)
        # Генерирация строковых значений
        with allure.step('Генерация случайных значений'):
            generated_lastname = self.generate_random()
            generated_firstname = self.generate_random()
        # Ввод строковых значений
        with allure.step('Заполнение обязательных полей ввода'):
            lastname_field.send_keys(generated_lastname)
            firstname_field.send_keys(generated_firstname)
        with allure.step('Заполнение поля ввода "Отчество"'):
            if middlename:
                middlename_field = self.wait_for_presence(loc.middlename_field)
                generated_middlename = self.generate_random()
                middlename_field.send_keys(generated_middlename)
        with allure.step('Заполнение поля ввода "Субъект"'):
            if subject:
                subject_field = self.wait_for_presence(loc.subject_field)
                generated_subject = self.generate_random()
                subject_field.send_keys(generated_subject)
        with allure.step('Заполнение поля ввода "Должность"'):
            if position:
                position_field = self.wait_for_presence(loc.position_field)
                generated_position = self.generate_random()
                position_field.send_keys(generated_position)
        with allure.step('Добавление изображения'):
            if image:
                image_button = self.wait_for_presence(loc.add_image_button)
                image_button.send_keys(loc.file_path)

        with allure.step('Подтверждение создания'):
            self.wait_for_clickable(loc.create_button_in_modal).click()
        new_lastname = self.wait_for_presence((By.XPATH, f'//*[text()="{generated_lastname}"]'))
        with allure.step('Проверка созданного участника с сгенерированным именем'):
            assert new_lastname.text.strip() == generated_lastname
        return new_lastname.text.strip()



    def update_participant(self, lastname):
        """Поиск участника по имени, очистка полей и генерация новых значений"""
        with allure.step('Поиск созданного участника и нажатие на него'):
            line_to_participant = self.wait_for_presence((By.XPATH, f'//*[text()="{lastname}"]'))
            line_to_participant.click()
        with allure.step('Открытие модального окна редактирования участника'):
            self.wait_for_clickable(loc.edit_button).click()
            lastname_field = self.wait_for_visible(loc.lastname_field)
            firstname_field = self.wait_for_visible(loc.firstname_field)
        with allure.step('Очистка полей ввода'):
            lastname_field.clear()
            firstname_field.clear()
        with allure.step('Генерация случайных значений'):
            generated_lastname = self.generate_random()
            generated_firstname = self.generate_random()
        with allure.step('Заполнение обязательных полей ввода'):
            lastname_field.send_keys(generated_lastname)
            firstname_field.send_keys(generated_firstname)
        with allure.step('Подтверждение создания'):
            self.wait_for_clickable(loc.save_button_in_modal).click()
        new_lastname = self.wait_for_presence((By.XPATH, f'//*[text()="{generated_lastname}"]'))
        with allure.step('Проверка отредактированного участника с новым сгенерированным именем'):
            assert new_lastname.text.strip() == generated_lastname
        return new_lastname.text.strip()

    def delete_participant(self, lastname):
        """Поиск участника по имении удаление"""
        with allure.step('Поиск созданного участника и нажатие на него'):
            line_to_participant = self.wait_for_presence((By.XPATH, f'//*[text()="{lastname}"]'))
            line_to_participant.click()
        with allure.step('Нажатие на кнопку удаления'):
            delete_button = self.wait_for_clickable(loc.delete_button)
            delete_button.click()
        with allure.step('Подтверждение удаления'):
            self.wait_for_clickable(loc.apply_delete_button).click()
        with allure.step('Проверка, что созданный ранее участник удален'):
            assert line_to_participant is not None
        return None

    def view_added_image(self, lastname):
        line_to_participant =self.wait_for_presence((By.XPATH, f'//*[text()="{lastname}"]'))
        line_to_participant.click()
        self.wait_for_presence(loc.view_image_button).click()
        if self.wait_for_presence(loc.modal_with_image):
            assert self.wait_for_presence(loc.modal_with_image).is_displayed()
        elif self.wait_for_presence(loc.no_image_notification):
            assert self.wait_for_presence(loc.no_image_notification).text == 'Для участника не загружено изображение!'
        elif self.wait_for_presence(loc.button_is_disable):
            assert self.wait_for_presence(loc.button_is_disable).get_attribute('disabled') == 'true'
        else:
            return None
        return None
