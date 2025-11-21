from selenium.common import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage
from pages.locators import configuration_locators as loc
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
import allure
import random
import string


class ConfigurationPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def go_to_lists_page(self):
        self.wait_for_clickable(loc.lists_page).click()
