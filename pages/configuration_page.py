from locators.configuration_locators import create_scheme_button
from pages.base_page import BasePage
from locators import configuration_locators as loc
from playwright.sync_api import Page
from time import sleep
import allure
import random
import string


class ConfigurationPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def go_to_lists_page(self):
        self.page.locator(loc.lists_page).click()

    def create_scheme(self):
        """Создание схемы"""
        name = "Scheme_" + str(random.randint(1000, 9999))
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
        dropdown = self.page.locator(loc.schemes_dropdown)
        dropdown.wait_for(state="visible")
        self.page.locator(loc.schemes_in_dropdown, has_text=name_scheme).first.click()

    def apply_scheme(self):
        """Применение схемы"""
        # Ждём, пока кнопка станет видимой и enabled
        button = self.page.locator(loc.apply_scheme_button, has_text="Применить")
        button.wait_for(state="visible")
        # button.wait_for(state="enabled")
        button.click()

    def edit_scheme(self, name_scheme):
        new_name_scheme = "Scheme_" + str(random.randint(1000, 9999))
        self.choice_scheme(name_scheme)
        self.page.locator(loc.edit_scheme_button).click()
        self.page.locator(loc.name_field_in_edit_scheme).fill(new_name_scheme)
        self.page.locator(loc.save_button_in_edit_scheme).click()


    def delete_scheme(self, name_scheme):
        pass

    def copy_scheme(self, name_scheme):
        pass

    def load_new_scheme(self, name_scheme):
        pass

    def download_scheme(self, name_scheme):
        pass
