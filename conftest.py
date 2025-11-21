import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
# from pages.auth_page import AuthPage
# from pages.configuration_page import ConfigurationPage
# from pages.lists_page import ListsPage
# from pages.profiles_page import ProfilesPage


@pytest.fixture(scope="function")
def browser_context():
    """Запускает браузер с нужными настройками и создаёт контекст (аналог incognito + сессии)."""
    with sync_playwright() as p:
        # Настройки для Chromium
        browser = p.chromium.launch(channel='chrome', headless=False, args=['--start-maximized', '--disable-cache', '--incognito'])
        # Создаём контекст (изолированная сессия, как incognito)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        yield context
        context.close()
        browser.close()