from time import sleep

import allure
import pytest


@allure.feature('Страница конфигурации зала')
class TestConfiguration:

    @pytest.fixture(scope='function')
    def prepare_profile(self, auth, profiles_page, configuration_page):
        """
        Создание профиля,
        переход в созданный профиль,
        переход на страницу профилей,
        удаление профиля
        """
        name = None
        try:
            name = profiles_page.create_profile()
            profiles_page.go_to_profile(name)
            yield name
        finally:
            configuration_page.go_to_back()
            profiles_page.delete_profile(name)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка создания схемы')
    @pytest.mark.configuration
    def test_create_scheme(self, prepare_profile, configuration_page):
        configuration_page.create_scheme()

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка выбора схемы в дропдауне и ее применение')
    @pytest.mark.configuration
    def test_choice_and_apply_scheme(self, prepare_profile, configuration_page):
        name_scheme = configuration_page.create_scheme()
        configuration_page.choice_scheme(name_scheme)
        configuration_page.apply_scheme()

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка редактирования названия схемы')
    @pytest.mark.configuration
    def test_edit_scheme(self, prepare_profile, configuration_page):
        name = configuration_page.create_scheme()
        configuration_page.edit_scheme(name)



    @allure.story('Негативные сценарии')
    @allure.title('Проверка максимального количества символов в названии схемы')
    @pytest.mark.configuration
    def test_create_max_number_of_characters_scheme(self, prepare_profile, configuration_page):
        configuration_page.create_max_number_of_characters_scheme()

    def test_delete_scheme(self, prepare_profile, configuration_page):
        name1 = configuration_page.create_scheme()
        name2 = configuration_page.create_scheme()
        name = configuration_page.create_scheme()
        name3 = configuration_page.create_scheme()
        configuration_page.delete_scheme(name)
        sleep(10)