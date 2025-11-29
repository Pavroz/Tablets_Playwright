from time import sleep

import allure


@allure.feature('Страница конфигурации зала')
class TestConfiguration:

    def test_create_scheme(self, auth, profiles_page, configuration_page):
        name = profiles_page.create_profile()
        profiles_page.go_to_profile(name)
        configuration_page.create_scheme()
        configuration_page.go_to_back()
        profiles_page.delete_profile(name)

    def test_choice_scheme(self, auth, profiles_page, configuration_page):
        name = profiles_page.create_profile()
        profiles_page.go_to_profile(name)
        name_scheme = configuration_page.create_scheme()
        configuration_page.choice_scheme(name_scheme)
        configuration_page.apply_scheme()
        configuration_page.go_to_back()
        profiles_page.delete_profile(name)