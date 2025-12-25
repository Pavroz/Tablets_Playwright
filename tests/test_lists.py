from time import sleep

import allure
import pytest
from constants import sort_cases, participant_cases

@allure.feature('Страница списка участников')
class TestLists:

    @pytest.fixture(scope='function')
    def preparation(self, auth, profiles_page, configuration_page, lists_page):
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
    @pytest.mark.parametrize("middlename, subject, position, image", participant_cases.CREATE_PARTICIPANT_CASES)
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
            self, preparation, lists_page,
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
    def test_update_participant(self, preparation, lists_page):
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
    def test_delete_participant(self, preparation, lists_page):
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
    def test_view_added_image(self, preparation, lists_page,
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
    def test_load_participant(self, preparation, lists_page):
        lists_page.load_participant()

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка получения всего списка участников')
    @pytest.mark.lists
    def test_get_all_participant(self, preparation, lists_page):
        lists_page.load_participant()
        lists_page.get_all_participant()

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка переключения страниц')
    @pytest.mark.lists
    def test_pagination_page(self, preparation, lists_page):
        lists_page.load_participant()
        lists_page.switch_page(10)
        lists_page.pagination_page()

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка переключения количества отображения данных')
    @pytest.mark.lists
    @pytest.mark.parametrize('value', [10, 20, 50, 100])
    def test_switch_page(self, preparation, lists_page, value):
        lists_page.load_participant()
        lists_page.switch_page(value=value)
        lists_page.pagination_page()

    @allure.story('Позитивные сценарии')
    @allure.title('Проверка поиска созданного участника по фамилии')
    @pytest.mark.lists
    # @pytest.mark.repeat(5)
    def test_search_participant_by_lastname(self, preparation, lists_page):
        lastname = lists_page.create_participant()
        lists_page.search_participant_by_lastname(lastname)

    # @allure.story('Позитивные сценарии')
    # @allure.title('Проверка сортировки по каждому значению')
    # @pytest.mark.lists
    # @pytest.mark.parametrize(
    #     'value', [
    #         'lastname',
    #         'firstname',
    #         'middlename',
    #         'subject',
    #         'position',
    #         'image'
    #     ]
    # )
    # def test_sort_up(self, preparation, sorting, value):
    #     sorting.sort_up(value=value)
    #
    # @allure.story('')
    # @allure.title('')
    # @pytest.mark.lists
    # @pytest.mark.parametrize(
    #     'value', [
    #         'lastname',
    #         'firstname',
    #         'middlename',
    #         'subject',
    #         'position',
    #         'image'
    #     ]
    # )
    # def test_sort_down(self,preparation, sorting, value):
    #     sorting.sort_down(value=value)
    #
    # @allure.story('')
    # @allure.title('')
    # @pytest.mark.lists
    # @pytest.mark.parametrize(
    #     'lastname, firstname, middlename, subject, position, image',
    #     [
    #         (None, None, None, None, None, None),  # без сортировки (дефолт)
    #          ("lastname", None, None, None, None, None),  # сортировка по фамилии
    #          (None, "firstname", None, None, None, None),  # по имени
    #          (None, None, "middlename", None, None, None),  # по отчеству
    #          (None, None, None, "subject", None, None),  # по субъекту
    #          (None, None, None, None, "position", None),  # по должности
    #          (None, None, None, None, None, "image"),  # по наличию изображения
    #          ("lastname", "firstname", None, None, None, None),  # фамилия + имя
    #          ("lastname", "firstname", "middlename", None, None, None),  # ФИО
    #          (None, None, None, "subject", "position", None),  # субъект + должность
    #          ("lastname", "firstname", "middlename", "subject", "position", "image")  # всё вместе
    #     ]
    # )
    # def test_sort_up(self, preparation, sorting, lastname, firstname, middlename, subject, position, image):
    #     sorting.sort(
    #         lastname=lastname,
    #         firstname=firstname,
    #         middlename=middlename,
    #         subject=subject,
    #         position=position,
    #         image=image
    #     )


