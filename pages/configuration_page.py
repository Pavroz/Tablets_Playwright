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
