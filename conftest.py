import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from pages.auth_page import AuthPage
from pages.configuration_page import ConfigurationPage
from pages.lists_page import ListsPage
from pages.profiles_page import ProfilesPage
from data import test_data


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(
            channel='chrome',
            headless=False,
            args=['--start-maximized', '--disable-cache', '--incognito']
        )
        context: BrowserContext = browser.new_context(no_viewport=True)
        page = context.new_page()
        yield page
        context.close()
        browser.close()

@pytest.fixture()
def auth_page(page: Page):
    """Инициализация страницы авторизации"""
    return AuthPage(page)

@pytest.fixture()
def profiles_page(page: Page):
    """Инициализация страницы профилей"""
    return ProfilesPage(page)

@pytest.fixture()
def lists_page(page: Page):
    """Инициализация страницы участников"""
    return ListsPage(page)

@pytest.fixture()
def configuration_page(page: Page):
    return ConfigurationPage(page)

@pytest.fixture()
def auth(auth_page):
    """Фикстура для авторизации"""
    auth_page.open() # т.к. в auth_page есть часть url, то через этот класс можно использовать open
    auth_page.auth_correct_login_and_password(test_data.login, test_data.password)
    yield auth_page  # возвращаем драйвер (или страницу)

