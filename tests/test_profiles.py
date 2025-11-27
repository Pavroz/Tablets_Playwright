import allure
import pytest


# ТЕСТЫ ПАРАЛЛЕЛИТЬ ТОЛЬКО НА ДВА ОКНА
@allure.feature('Страница профилей')
class TestProfiles:

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка создания профиля')
    @pytest.mark.profiles
    def test_create_profile(self, auth, profiles_page):
        name = profiles_page.create_profile()
        profiles_page.delete_profile(name)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка удаления профиля')
    @pytest.mark.profiles
    def test_delete_profile(self, auth, profiles_page):
        name = profiles_page.create_profile()
        profiles_page.delete_profile(name)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка изменения имени профиля')
    @pytest.mark.profiles
    def test_edit_name_profile(self, auth, profiles_page):
        name = profiles_page.create_profile()
        new_name_profile = profiles_page.edit_name_profile(name)
        profiles_page.delete_profile(new_name_profile)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка изменения описания профиля')
    @pytest.mark.profiles
    def test_edit_description_profile(self, auth, profiles_page):
        name = profiles_page.create_profile()
        profiles_page.edit_description_profile(name)
        # sleep(2)
        profiles_page.delete_profile(name)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка изменения имени и описания профиля')
    @pytest.mark.profiles
    def test_edit_full_profile(self, auth, profiles_page):
        name = profiles_page.create_profile()
        new_name_profile = profiles_page.edit_full_profile(name)
        profiles_page.delete_profile(new_name_profile)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка копирования профиля')
    @pytest.mark.profiles
    def test_copy_profile(self, auth, profiles_page):
        name = profiles_page.create_profile()
        new_name_profile = profiles_page.copy_profile(name)
        profiles_page.delete_profile(name)
        profiles_page.delete_profile(new_name_profile)

    @allure.story('Негативные сценарии')
    @allure.title('Проверка создания профиля с существующим наименованием')
    @pytest.mark.profiles
    def test_create_existing_profile(self, auth, profiles_page):
        name = profiles_page.create_profile()
        profiles_page.create_existing_profile(name)
        profiles_page.delete_profile(name)

    @allure.story('Негативные сценарии')
    @allure.title('Проверка копирования профиля с существующим наименованием')
    @pytest.mark.profiles
    def test_copy_existing_profile(self, auth, profiles_page):
        name = profiles_page.create_profile()
        profiles_page.copy_existing_profile(name)
        profiles_page.delete_profile(name)

    @allure.story('Негативные сценарии')
    @allure.title('Проверка максимального количества символов в имени профиля')
    @pytest.mark.profiles
    def test_create_max_number_of_characters_profile(self, auth, profiles_page):
        profiles_page.create_max_number_of_characters_profile()

    @allure.story('Негативные сценарии')
    @allure.title('Проверка дизейбла кнопки сохранения при пустом наименовании профиля')
    @pytest.mark.profiles
    def test_create_an_empty_profile(self, auth, profiles_page):
        profiles_page.create_an_empty_profile()