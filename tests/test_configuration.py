from time import sleep

import allure
import pytest

@pytest.mark.skip
@allure.feature('Страница конфигурации зала')
class TestConfiguration:

    @pytest.fixture(scope='function')
    def preparation(self, auth, profiles_page, configuration_page):
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
    def test_create_scheme(self, preparation, configuration_page):
        configuration_page.create_scheme()

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка выбора схемы в дропдауне и ее применение')
    @pytest.mark.configuration
    def test_choice_and_apply_scheme(self, preparation, configuration_page):
        name_scheme = configuration_page.create_scheme()
        configuration_page.choice_scheme(name_scheme)
        configuration_page.apply_scheme()

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка редактирования названия схемы')
    @pytest.mark.configuration
    def test_edit_scheme(self, preparation, configuration_page):
        name = configuration_page.create_scheme()
        configuration_page.edit_scheme(name)

    @allure.story('Негативные сценарии')
    @allure.title('Проверка максимального количества символов в названии схемы')
    @pytest.mark.configuration
    def test_create_max_number_of_characters_scheme(self, preparation, configuration_page):
        configuration_page.create_max_number_of_characters_scheme()


    @allure.story('Позитивные сценарии')
    @allure.title('Проверка')
    @pytest.mark.configuration
    def test_delete_scheme(self, preparation, configuration_page):
        name = configuration_page.create_scheme()
        configuration_page.delete_scheme(name)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка')
    @pytest.mark.configuration
    def test_copy_scheme(self, preparation, configuration_page):
        name = configuration_page.create_scheme()
        configuration_page.copy_scheme(name)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка')
    @pytest.mark.configuration
    def test_load_new_scheme(self, preparation, configuration_page):
        name = configuration_page.create_scheme()
        configuration_page.load_new_scheme(name)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка')
    @pytest.mark.configuration
    def test_download_scheme(self, preparation, configuration_page):
        name = configuration_page.create_scheme()
        configuration_page.download_scheme(name)

    # Запуск теста - pytest -v -s -m repeat --count=5 -n 5
    # @pytest.mark.repeat(5)  # повторить 5 раз
    @allure.story('Позитивные сценарии')
    @allure.title('Проверка')
    @pytest.mark.configuration
    def test_create_place(self, preparation, configuration_page):
        name = configuration_page.create_scheme()
        configuration_page.create_place(name)
        sleep(1)

