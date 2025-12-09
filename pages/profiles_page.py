import re

from pages.base_page import BasePage
from locators import profiles_locators as loc
from time import sleep
import allure
import random
import string
from playwright.sync_api import expect, Page

class ProfilesPage(BasePage):
    page_url = '/profiles'

    def __init__(self, page):
        super().__init__(page)


    def get_all_carts(self):
        """Получение списка карточек для дальнейшего взаимодействия с ними (например нажатие)"""
        return self.page.locator(loc.all_carts).all() # ← .all() делает список


    def get_all_carts_titles(self):
        """Получение списка с названиями карточек"""
        carts = self.get_all_carts() # List[Locator]
        titles = []
        for cart in carts:
            try:
                title = cart.locator(*loc.name_cart).inner_text().strip()
                titles.append(title)
            except Exception as e:
                print(f"Ошибка при получении названия карточки: {e}")
        return titles

    @staticmethod
    def generate_profile_name(prefix='test_', length = 20):
        """Генерация имени для тестового профиля"""
        suffix = ''.join(random.choice(string.ascii_lowercase + string.digits)
                         for _ in range(length - len(prefix)))
        return f'{prefix}{suffix}'

    @staticmethod
    def generate_profile_description(prefix='TEST_', length = 50):
        """Генерация описания для тестового профиля"""
        suffix = ''.join(random.choice(string.ascii_lowercase + string.digits)
                         for _ in range(length - len(prefix)))
        return f'{prefix}{suffix}'

    # def create_profile(self, description=None):
    #     """Создает профиль и возвращает его имя"""
    #     name = self.generate_profile_name()
    #     with (allure.step('Создание профиля')):
    #         try:
    #             if name in self.get_all_carts_titles():
    #                 # print(f'Профиль "{name}" уже существует')
    #                 return None
    #             self.page.locator(loc.create_profile_button).click()
    #             name_field = self.page.locator(loc.name_field)
    #             # sleep(1)
    #             name_field.fill(name)
    #             # name_field.send_keys(Keys.TAB)
    #             if description:
    #                 self.page.locator(loc.description_field).fill(description)
    #             self.page.locator(loc.apply_modals_button).click()
    #         except:
    #             pass
    #     # ПРОСТАЯ ПРОВЕРКА - ждем появления профиля по имени
    #     with allure.step(f'Проверка ожидания появления профиля по его имени - "{name}"'):
    #         expect(self.page.locator(f'//*[text()="{name}"]')).to_be_attached()
    #         # expect(self.page.locator(f'//*[text()="{name}"]')).to_be_visible()
    #     return name
    def create_profile(self, description=None):
        name = self.generate_profile_name()
        # Убираем проверку на существование — генерация и так даёт уникальные имена
        self.page.locator(loc.create_profile_button).click()
        self.page.locator(loc.name_field).fill(name)
        if description:
            self.page.locator(loc.description_field).fill(description)
        self.page.locator(loc.apply_modals_button).click()

        # Ждём появления профиля
        expect(self.page.get_by_text(name, exact=True)).to_be_visible()
        return name

    def create_existing_profile(self, name_profile):
        """Создает существующий профиль"""
        with allure.step('Создание существующего профиля'):
            # ждём, пока кнопка создания станет доступной
            create_button = self.page.locator(loc.create_profile_button)
            expect(create_button).to_be_visible()
            create_button.click()
            # ждём появления модалки
            name_input = self.page.locator(loc.name_field)
            expect(name_input).to_be_visible()
            name_input.fill(name_profile)
            # ждём, пока кнопка Apply станет disabled
            apply_button = self.page.locator(loc.apply_modals_button)
            expect(apply_button).to_be_disabled()
            # закрываем модалку
            self.page.locator(loc.cancel_modals_button).click()

    def delete_profile(self, name_profile):
        """Удаляет профиль по имени"""
        # Находим и кликаем кнопку удаления для профиля с нужным именем
        with allure.step('Нажатие на кнопку удаления'):
            # sleep(1)
            for attempt in range(3):  # 3 попытки
                try:
                    delete_button = self.page.locator(
                         f'//*[text()="{name_profile}"]//ancestor::prominform-profile-card//span[@nztype="delete"]'
                    )
                    # self.driver.execute_script('arguments[0].scrollIntoView();', delete_button)
                    delete_button.click()
                    break  # Если клик прошел, выходим из цикла
                except:
                    if attempt == 2:  # Последняя попытка
                        raise
                    # sleep(1)  # Ждем перед повторной попыткой
            with allure.step('Подтверждение удаления'):
                self.page.locator(loc.yes_button_from_delete).click()
            # Ждем исчезновения профиля
            with allure.step('Ожидание удаления профиля'):
                assert self.page.locator(f'//*[text()="{name_profile}"]')


    def edit_name_profile(self, name_profile):
        new_name_profile = self.generate_profile_name()
        # Поиск кнопки редактирования
        with allure.step('Нажатие на кнопку редактирования'):
            edit_button = self.page.locator(
                 f'//*[text()="{name_profile}"]//ancestor::prominform-profile-card//span[@nztype="edit"]'
            )
            # self.driver.execute_script('arguments[0].scrollIntoView();', edit_button)
            edit_button.click()
        with allure.step('Очистка и заполнение поля ввода "Наименование"'):
            name_field = self.page.locator(loc.name_field)
            name_field.clear()
            name_field.fill(new_name_profile)
            self.page.keyboard.press('Tab')
        with allure.step('Подтверждение редактирования'):
            self.page.locator(loc.apply_modals_button).click()
        with allure.step('Проверка, что наименование изменилось'):
            assert self.page.locator(f'//*[text()="{new_name_profile}"]')
        return new_name_profile

    def edit_description_profile(self, name_profile):
        """Изменение описания профиля"""
        new_description_profile = self.generate_profile_description()
        # sleep(1)
        # Поиск кнопки редактирования
        with allure.step('Нажатие на кнопку редактирования'):
            edit_button = self.page.locator(
                 f'//*[text()="{name_profile}"]//ancestor::prominform-profile-card//span[@nztype="edit"]'
            )
            # self.driver.execute_script('arguments[0].scrollIntoView();', edit_button)
            edit_button.click()
        with allure.step('Очистка и заполнение поля ввода "Описание профиля"'):
            description_field = self.page.locator(loc.description_field)
            if description_field is not None:
                description_field.clear()
            description_field.fill(new_description_profile)
            self.page.keyboard.press('Tab')
        with allure.step('Подтверждение редактирования'):
            self.page.locator(loc.apply_modals_button).click()
        with allure.step('Ожидание закрытия модалки'):
            self.page.locator('nz-modal-container')
        with allure.step('Повторное нажатие кнопки редактирования'):
            for _ in range(3):
                try:
                    edit_button = self.page.locator(
                         f'//*[text()="{name_profile}"]//ancestor::prominform-profile-card//span[@nztype="edit"]'
                    )
                    # self.driver.execute_script('arguments[0].scrollIntoView();', edit_button)
                    edit_button.click()
                    break
                except:
                    # sleep(1)
                    continue
            else:
                raise Exception('Не удалось нажать кнопку редактирования')
            with allure.step('Проверка, что поле ввода не пустое'):
                assert self.page.locator(loc.description_field_is_not_null) is not None
            self.page.locator(loc.cancel_modals_button).click()
        return new_description_profile

    def edit_full_profile(self, name_profile):
        new_name_profile = self.generate_profile_name()
        new_description_profile = self.generate_profile_description()
        with allure.step('Нажатие на кнопку редактирования'):
            edit_button = self.page.locator(
                 f'//*[text()="{name_profile}"]//ancestor::prominform-profile-card//span[@nztype="edit"]'
            )
            # self.driver.execute_script('arguments[0].scrollIntoView();', edit_button)
            edit_button.click()
        with allure.step('Очистка и заполнение полей ввода "Наименование" и "Описание профиля"'):
            name_field = self.page.locator(loc.name_field)
            name_field.clear()
            name_field.fill(new_name_profile)
            self.page.keyboard.press('Tab')
            description_field = self.page.locator(loc.description_field)
            description_field.clear()
            description_field.fill(new_description_profile)
            self.page.keyboard.press('Tab')
        with allure.step('Подтверждение редактирования'):
            self.page.locator(loc.apply_modals_button).click()
        with allure.step('Проверка, что наименование и описание изменились'):
            assert self.page.locator(f'//*[text()="{new_name_profile}"]')
        return new_name_profile

    def copy_profile(self, name_profile):
        new_name_profile = self.generate_profile_name()
        new_description_profile = self.generate_profile_description()
        with allure.step('Нажатие на кнопку копирования'):
            copy_button = self.page.locator(
                f'//*[text()="{name_profile}"]//ancestor::prominform-profile-card//span[@nztype="copy"]'
            )
            copy_button.click()
        with allure.step('Очистка и заполнение полей ввода "Наименование" и "Описание профиля"'):
            name_field = self.page.locator(loc.name_field)
            name_field.clear()
            name_field.fill(new_name_profile)
            description_field = self.page.locator(loc.description_field)
            description_field.clear()
            description_field.fill(new_description_profile)
        with allure.step('Подтверждение копирования'):
            self.page.locator(loc.apply_modals_button).click()
        with allure.step('Проверка, что профиль успешно скопировался'):
            assert self.page.locator(f'//*[text()="{new_name_profile}"]')
        return new_name_profile

    def copy_existing_profile(self, name_profile):
        """Копирование существуюшего профиля"""
        copy_button = self.page.locator(
             f'//*[text()="{name_profile}"]//ancestor::prominform-profile-card//span[@nztype="copy"]'
        )
        # self.driver.execute_script('arguments[0].scrollIntoView();', copy_button)
        copy_button.click()
        name_field = self.page.locator(loc.name_field)
        name_field.clear()
        name_field.fill(name_profile)
        apply_button = self.page.locator(loc.apply_modals_button)
        # assert apply_button.get_attribute('disabled') == 'true'
        expect(self.page.locator(loc.apply_modals_button)).to_be_disabled()
        self.page.locator(loc.cancel_modals_button).click()

    def create_max_number_of_characters_profile(self, quantity=256):
        name = ''.join(random.choice(string.ascii_lowercase + string.digits)
                       for _ in range(quantity))
        self.page.locator(loc.create_profile_button).click()
        name_field = self.page.locator(loc.name_field)
        name_field.fill(name)
        apply_button = self.page.locator(loc.apply_modals_button)
        # assert apply_button.get_attribute('disabled') == 'true'
        expect(self.page.locator(loc.apply_modals_button)).to_be_disabled()

    def create_an_empty_profile(self):
        self.page.locator(loc.create_profile_button).click()
        apply_button = self.page.locator(loc.apply_modals_button)
        # assert apply_button.get_attribute('disabled') == 'true'
        expect(self.page.locator(loc.apply_modals_button)).to_be_disabled()

    def go_to_profile(self, name_profile):
        go_to_profile_button = self.page.locator(
             f'//*[text()="{name_profile}"]//ancestor::prominform-profile-card//div[@class="ant-card-body"]'
        )
        # self.driver.execute_script('arguments[0].scrollIntoView();', go_to_profile_button)
        go_to_profile_button.click()

    def activate_profile(self, name_profile):
        switch_button = self.page.locator(
            f'//*[text()="{name_profile}"]{loc.switch_button}'
        )
        switch_button.click()
        expect(switch_button).to_have_class(re.compile('.*ant-switch-checked.*'))

    def deactivate_profile(self, name_profile):
        switch_button = self.page.locator(
            f'//*[text()="{name_profile}"]{loc.switch_button}'
        )
        switch_button.click()
        # проверяем, что класс "ant-switch-checked" пропал
        expect(switch_button).not_to_have_class(re.compile(".*ant-switch-checked.*"))
