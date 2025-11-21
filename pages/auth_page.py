from time import sleep
from pages.base_page import BasePage
from locators import auth_locators as loc
from locators import profiles_locators as locp
import allure
from playwright.async_api import expect

class AuthPage(BasePage):
    page_url = '/auth'

    def __init__(self, driver):
        super().__init__(driver)

    def auth_correct_login_and_password(self, login, password):
        with allure.step(f'Ввод логина "{login}"'):
            self.page.locator(loc.login).fill(login)
        with allure.step(f'Ввод пароля "{password}"'):
            self.page.locator(loc.password).fill(password)
        with allure.step('Нажатие на кнопку авторизации'):
            self.page.locator(loc.auth_button).click()
            sleep(1)
        current_url = self.page.url
        with allure.step('Проверка успешной авторизации'):
            # assert current_url == 'http://arm-tablets.01-bfv-server.stroki.loc/profiles'
            expect(self.page.locator(locp.all_carts)).to_have_count(0)
        return True


    def auth_incorrect_login(self, login, password):
        with allure.step(f'Ввод логина "{login}"'):
            self.page.locator(loc.login).fill(login)
        with allure.step(f'Ввод пароля "{password}"'):
            self.page.locator(loc.password).fill(password)
        with allure.step('Нажатие на кнопку авторизации'):
            self.page.locator(loc.auth_button).click()
        notification_text = self.page.locator(loc.notification).inner_text()
        with allure.step('Проверка текста ошибки'):
            assert notification_text == f"Не удалось авторизоваться: \"Пользователь с логином '{login}' не найден\""

    def auth_incorrect_password(self, login, password):
        with allure.step(f'Ввод логина "{login}"'):
            self.page.locator(loc.login).fill(login)
        with allure.step(f'Ввод пароля "{password}"'):
            self.page.locator(loc.password).fill(password)
        with allure.step('Нажатие на кнопку авторизации'):
            self.page.locator(loc.auth_button).click()
        notification_text = self.page.locator(loc.notification).inner_text()
        with allure.step('Проверка текста ошибки'):
            assert notification_text == f'Не удалось авторизоваться: "Неверные учетные данные"'


    def auth_active_recovery_conf(self, login, password):
        with allure.step(f'Ввод логина "{login}"'):
            self.page.locator(loc.login).fill(login)
        with allure.step(f'Ввод пароля "{password}"'):
            self.page.locator(loc.password).fill(password)
        recovery_active = self.page.locator(loc.recovery_conf_active)
        with allure.step(f'Проверка, что кнопка активна'):
            assert "ant-switch-checked" in recovery_active.get_attribute("class")
        # sleep(2)
        with allure.step('Нажатие на кнопку авторизации'):
            self.page.locator(loc.auth_button).click()

    def auth_inactive_recovery_conf(self, login, password):
        with allure.step(f'Ввод логина "{login}"'):
            self.page.locator(loc.login).fill(login)
        with allure.step(f'Ввод пароля "{password}"'):
            self.page.locator(loc.password).fill(password)
        recovery_active = self.page.locator(loc.recovery_conf_active)
        with allure.step(f'Проверка, что кнопка активна'):
            assert "ant-switch-checked" in recovery_active.get_attribute("class")
#         sleep(2)
        with allure.step(f'Деактивация кнопки'):
            recovery_active.click()
        with allure.step(f'Проверка, что кнопка деактивирована'):
            assert "ant-switch-checked" not in recovery_active.get_attribute("class")
#         sleep(2)
        with allure.step('Нажатие на кнопку авторизации'):
            self.page.locator(loc.auth_button).click()

    def auth_empty_fields(self):
        """Авторизация с пустым логином и паролем"""
        with allure.step('Нажатие кнопки авторизации'):
            self.page.locator(loc.auth_button).click()
        login_message = self.page.locator(loc.login_validation)
        # print(login_message)
        password_message = self.page.locator(loc.password_validation)
        # print(password_message)
        with allure.step('Проверка валидации пустого логина'):
            # assert login_message.text == 'Пожалуйста, введите логин!'
            assert login_message.inner_text() is not None
        with allure.step('Проверка валидации пустого пароля'):
            # assert password_message.text == 'Пожалуйста, введите пароль!'
            assert password_message.inner_text() is not None
        return True