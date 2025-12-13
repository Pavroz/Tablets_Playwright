from playwright.sync_api import Page


class BasePage:
    base_url = 'http://arm-tablets.01-bfv-server.stroki.loc'
    page_url = None

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        """Открытие браузера"""
        if self.page_url:
            self.page.goto(f'{self.base_url}{self.page_url}')
        else:
            self.page.goto(self.base_url)

    def go_to_back(self):
        """Возвращение на страницу списка профилей"""
        back_button = 'nz-page-header i[nztype="left"]'
        self.page.locator(back_button).click()