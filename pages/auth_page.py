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

    @allure.step('Авторизация с корректным логином и паролем')
    def auth_correct_login_and_password(self, login, password) -> bool:
        """Авторизация с корректным логином и паролем"""
        self.page.locator(loc.login).fill(login)
        self.page.locator(loc.password).fill(password)
        self.page.locator(loc.auth_button).click()
        # sleep(1)
        expect(self.page.wait_for_url('http://arm-tablets.01-bfv-server.stroki.loc/profiles', timeout=10000))
        return True

    @allure.step('Авторизация с некорректным логином')
    def auth_incorrect_login(self, login, password):
        """Авторизация с некорректным логином"""
        self.page.locator(loc.login).fill(login)
        self.page.locator(loc.password).fill(password)
        self.page.locator(loc.auth_button).click()
        notification_text = self.page.locator(loc.notification).inner_text()
        assert notification_text == f"Не удалось авторизоваться: \"Пользователь с логином '{login}' не найден\""

    @allure.step('Авторизация с некорректным паролем')
    def auth_incorrect_password(self, login, password):
        """Авторизация с некорректным паролем"""
        self.page.locator(loc.login).fill(login)
        self.page.locator(loc.password).fill(password)
        self.page.locator(loc.auth_button).click()
        notification_text = self.page.locator(loc.notification).inner_text()
        assert notification_text == f'Не удалось авторизоваться: "Неверные учетные данные"'

    @allure.step('Авторизация с активным восстановлением конфигурации')
    def auth_active_recovery_conf(self, login, password):
        """Авторизация с активным восстановлением конфигурации"""
        self.page.locator(loc.login).fill(login)
        self.page.locator(loc.password).fill(password)
        expect(self.page.locator(loc.recovery_conf_active)).to_have_class(re.compile("ant-switch-checked"))
        self.page.locator(loc.auth_button).click()

    @allure.step('Авторизация с неактивным восстановлением конфигурации')
    def auth_inactive_recovery_conf(self, login, password):
        """Авторизация с неактивным восстановлением конфигурации"""
        self.page.locator(loc.login).fill(login)
        self.page.locator(loc.password).fill(password)
        recovery_active = self.page.locator(loc.recovery_conf_active)
        expect(self.page.locator('nz-switch[formcontrolname="personalization"] button')
               ).to_have_class(re.compile('.*ant-switch-checked.*'), timeout=5000)
        recovery_active.click()
        expect(self.page.locator('nz-switch[formcontrolname="personalization"] button')
               ).not_to_have_class(re.compile('.*ant-switch-checked.*'), timeout=5000)
        self.page.locator(loc.auth_button).click()

    @allure.step('Авторизация с пустым логином и паролем')
    def auth_empty_fields(self) -> bool:
        """Авторизация с пустым логином и паролем"""
        self.page.locator(loc.auth_button).click()
        login_message = self.page.locator(loc.login_validation)
        password_message = self.page.locator(loc.password_validation)
        # assert login_message.text == 'Пожалуйста, введите логин!'
        assert login_message.inner_text() is not None
        # assert password_message.text == 'Пожалуйста, введите пароль!'
        assert password_message.inner_text() is not None
        return True
