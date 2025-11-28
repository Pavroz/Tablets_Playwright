# Список профилей
all_carts = "prominform-profile-card" # Весь список профилей
name_cart = ".profile-card__title span[nz-typography]" # Получение имени профиля

# get_all_profiles = (By.CSS_SELECTOR, 'div prominform-profile-card') # карточки профилей
# profile_name_in_card = (By.CSS_SELECTOR, 'span.ant-typography') # название внутри карточки

# Кнопки создания, редактирования, копирования и активации профиля
create_profile_button = '//span[contains(text(), "Создать профиль")]'
edit_profile_button = 'span[nztype="edit"]'
copy_profile_button = 'span[nztype="copy"]'
activate_profile_button = 'nz-switch[nzsize="small"]'

# Кнопка удаления профиля с подтверждением
delete_profile_button = 'span[nztype="delete"]'
yes_button_from_delete = '//span[contains(text(), "Да")]'

# Поля в модалке
name_field = 'input[formcontrolname="name"]'
description_field = 'textarea[formcontrolname="description"]'
description_field_is_not_null = 'textarea.ng-untouched'

# Подтверждение изменения
apply_modals_button = '.modal-footer button[nztype="primary"]'
# Отмена изменений
cancel_modals_button = '//span[text()="Отмена"]'

# activate_button = '.ant-switch-small'
activate_button = '//button[@class="ant-switch ant-switch-small"]'
is_active_button = '.ant-switch-checked'
deactivate_button = '//button[@class="ant-switch ant-switch-small ant-switch-checked"]'
is_inactive_button = '.ant-switch-handle'
switch_button = '//ancestor::prominform-profile-card//button[contains(@class,"ant-switch")]'