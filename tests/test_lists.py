from time import sleep

import allure
import pytest


@allure.feature('Страница списка участников')
class TestLists:

    @pytest.fixture(scope='function')
    def prepare_profile_and_open_lists(self, auth, profiles_page, configuration_page, lists_page):
        """
        Создание профиля,
        переход в созданный профиль,
        переход на страницу списка участников,
        переход на страницу профилей,
        удаление профиля
        """
        name = None
        try:
            name = profiles_page.create_profile()
            profiles_page.go_to_profile(name)
            configuration_page.go_to_lists_page()
            yield
        finally:
            lists_page.go_to_back()
            profiles_page.delete_profile(name)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка создания участника')
    @pytest.mark.lists
    @pytest.mark.parametrize("middlename, subject, position, image",
        [
            (None, None, None, None),  # только обязательные поля
            ("middlename", None, None, None),  # + отчество
            (None, "subject", None, None),  # + субъект
            (None, None, "position", None),  # + должность
            (None, None, None, "image"),  # + изображение
            ("middlename", "subject", "position", "image"),  # всё вместе
        ]
    )
    # @pytest.mark.parametrize(
    #     "middlename, subject, position, image",
    #     [
    #         (None, None, None, None),
    #         ("middlename", None, None, None),
    #         (None, "subject", None, None),
    #         (None, None, "position", None),
    #         (None, None, None, "image"),
    #
    #         ("middlename", "subject", None, None),
    #         ("middlename", None, "position", None),
    #         ("middlename", None, None, "image"),
    #         (None, "subject", "position", None),
    #         (None, "subject", None, "image"),
    #         (None, None, "position", "image"),
    #
    #         ("middlename", "subject", "position", None),
    #         ("middlename", "subject", None, "image"),
    #         ("middlename", None, "position", "image"),
    #         (None, "subject", "position", "image"),
    #
    #         ("middlename", "subject", "position", "image"),  # все заполнены
    #     ]
    # )
    def test_created_participant(
            self, prepare_profile_and_open_lists, lists_page,
            middlename, subject, position, image
    ):
        # Передаём параметры в метод
        lists_page.create_participant(
            middlename=middlename,
            subject=subject,
            position=position,
            image=image
        )

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка редактирования участника')
    @pytest.mark.lists
    def test_update_participant(self, prepare_profile_and_open_lists, lists_page):
        name_participant = lists_page.create_participant()
        lists_page.update_participant(name_participant)
        ## Вариант с try - finally, чтобы профиль всегда удалялся
        # name = None
        # try:
        #     name = profiles_page.create_profile()
        #     profiles_page.go_to_profile(name)
        #     configuration_page.go_to_lists_page()
        #     name_participant = lists_page.create_participant()
        #     lists_page.update_participant(name_participant)
        #     # lists_page.go_to_back()
        # finally:
        #         try:
        #             lists_page.go_to_back()
        #             profiles_page.delete_profile(name)
        #         except Exception as e:
        #             print(f"Не удалось удалить профиль '{name}': {e}")

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка удаления участника')
    @pytest.mark.lists
    def test_delete_participant(self, prepare_profile_and_open_lists, lists_page):
        name_participant = lists_page.create_participant()
        lists_page.delete_participant(name_participant)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка добавленного изображения')
    @pytest.mark.lists
    @pytest.mark.parametrize(
        "middlename, subject, position, image",
        [
            (None, None, None, None),
            ("middlename", "subject", "position", "image"),
        ]
    )
    def test_view_added_image(self, prepare_profile_and_open_lists, lists_page,
                              middlename, subject, position, image):
        name_participant = lists_page.create_participant(
            middlename=middlename,
            subject=subject,
            position=position,
            image=image
        )
        lists_page.view_added_image(name_participant)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка загрузки участников из csv файла')
    @pytest.mark.lists
    def test_load_participant(self, prepare_profile_and_open_lists, lists_page):
        lists_page.load_participant()

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка получения всего списка участников')
    @pytest.mark.lists
    def test_get_all_participant(self, prepare_profile_and_open_lists, lists_page):
        lists_page.load_participant()
        lists_page.get_all_participant()

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка переключения страниц')
    @pytest.mark.lists
    def test_pagination_page(self, prepare_profile_and_open_lists, lists_page):
        lists_page.load_participant()
        lists_page.switch_page(10)
        lists_page.pagination_page()

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка переключения количества отображения данных')
    @pytest.mark.lists
    @pytest.mark.parametrize('value', [10, 20, 50, 100])
    def test_switch_page(self, prepare_profile_and_open_lists, lists_page, value):
        lists_page.load_participant()
        lists_page.switch_page(value=value)
        lists_page.pagination_page()

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка поиска созданного участника по фамилии')
    @pytest.mark.lists
    # @pytest.mark.repeat(5)
    def test_search_participant_by_lastname(self, prepare_profile_and_open_lists, lists_page):
        lastname = lists_page.create_participant()
        lists_page.search_participant_by_lastname(lastname)

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка сортировки по каждому значению')
    @pytest.mark.lists
    @pytest.mark.parametrize(
        'value', [
            'lastname',
            'firstname',
            'middlename',
            'subject',
            'position',
            'image'
        ]
    )
    def test_sort_up(self, prepare_profile_and_open_lists, sorting, value):
        sorting.sort_up(value=value)
