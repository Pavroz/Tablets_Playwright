import re
from time import sleep
from pages.base_page import BasePage
from locators import auth_locators as loc
import allure
from playwright.sync_api import expect

class AuthPage(BasePage):
    page_url = '/auth'

    def __init__(self, page):
        super().__init__(page)


    def __fill_login_and_password(self, login: str, password: str):
        self.page.locator(loc.login).fill(login)
        self.page.locator(loc.password).fill(password)

    def __click_login(self):
        self.page.locator(loc.login).click()


    @allure.step('Авторизация с корректным логином и паролем')
    def auth_correct_login_and_password(self, login, password) -> bool:
        """Авторизация с корректным логином и паролем"""
        self.__fill_login_and_password(login, password)
        self.__click_login()
        self.page.wait_for_url('http://arm-tablets.01-bfv-server.stroki.loc/profiles', timeout=10000)
        return True

    @allure.step('Авторизация с некорректным логином')
    def auth_incorrect_login(self, login, password):
        """Авторизация с некорректным логином"""
        self.__fill_login_and_password(login, password)
        self.__click_login()
        notification_text = self.page.locator(loc.notification).inner_text()
        assert notification_text == f"Не удалось авторизоваться: \"Пользователь с логином '{login}' не найден\""

    @allure.step('Авторизация с некорректным паролем')
    def auth_incorrect_password(self, login, password):
        """Авторизация с некорректным паролем"""
        self.__fill_login_and_password(login, password)
        self.__click_login()
        notification_text = self.page.locator(loc.notification).inner_text()
        assert notification_text == f'Не удалось авторизоваться: "Неверные учетные данные"'

    @allure.step('Авторизация с активным восстановлением конфигурации')
    def auth_active_recovery_conf(self, login, password):
        """Авторизация с активным восстановлением конфигурации"""
        self.__fill_login_and_password(login, password)
        expect(self.page.locator(loc.recovery_conf_active)).to_have_class(re.compile("ant-switch-checked"))
        self.__click_login()

    @allure.step('Авторизация с неактивным восстановлением конфигурации')
    def auth_inactive_recovery_conf(self, login, password):
        """Авторизация с неактивным восстановлением конфигурации"""
        self.__fill_login_and_password(login, password)
        recovery_active = self.page.locator(loc.recovery_conf_active)
        expect(self.page.locator('nz-switch[formcontrolname="personalization"] button')
               ).to_have_class(re.compile('.*ant-switch-checked.*'), timeout=5000)
        recovery_active.click()
        expect(self.page.locator('nz-switch[formcontrolname="personalization"] button')
               ).not_to_have_class(re.compile('.*ant-switch-checked.*'), timeout=5000)
        self.__click_login()

    @allure.step('Авторизация с пустым логином и паролем')
    def auth_empty_fields(self) -> bool:
        """Авторизация с пустым логином и паролем"""
        self.__click_login()
        login_message = self.page.locator(loc.login_validation)
        password_message = self.page.locator(loc.password_validation)
        # assert login_message.text == 'Пожалуйста, введите логин!'
        assert login_message.inner_text() is not None
        # assert password_message.text == 'Пожалуйста, введите пароль!'
        assert password_message.inner_text() is not None
        return True
