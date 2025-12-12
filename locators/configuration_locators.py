import os

lists_page = '//div[text()=" Списки участников "]'

# Создание схемы
create_scheme_button = 'i.anticon.anticon-plus.ng-star-inserted'
name_field = 'input[formcontrolname="name"]'
add_file_button = '//nz-upload//input[@type="file"]'
create_button = 'nz-modal-container [nztype="primary"]'
cancel_button = '//span[text()="Отмена"]'
scheme_path = os.getcwd() + r'\data\Scheme.svg'

# Дропдаун со схемами
schemes_selector = '.ant-select-selector' # Кнопка с дропдауном
schemes_dropdown = '.ant-select-dropdown' # Дропдаун
schemes_in_dropdown = '.ant-select-item-option-content'

# Применение схемы
apply_scheme_button = 'button[nztype="primary"]'

# Редактирование схемы
edit_scheme_button = '(//i[@class="anticon anticon-edit ng-star-inserted"])[1]'
name_field_in_edit_scheme = 'input[formcontrolname="name"]'
save_button_in_edit_scheme = '//span[text()=" Сохранить "]'
cancel_button_in_edit_scheme = '//span[text()="Отмена"]'

# Удаление схемы
delete_scheme_button = '.anticon-delete.ng-star-inserted'
yes_scheme_button = '//span[text()=" Да "]'
no_scheme_button = '//span[text()=" Нет "]'

# Копирование схемы
copy_scheme_button = '.anticon-copy'
nz_modal_container = 'nz-modal-container'
name_field_in_copy_scheme = 'input[formcontrolname="name"]'
copy_button = '//span[text()=" Копировать "]'

# Загрузка новой схемы
load_new_scheme_button = '.anticon-folder-open'
new_scheme_path = os.getcwd() + r'\data\New_scheme.svg'
loader_on_button = 'i[nztype="loading"]'

# Скачаивание схемы
download_scheme_button = '.anticon-save'

# Схема зала
scheme = '#svg-border'
edit_switch_off = '.ant-switch-small'
edit_switch_on = '.ant-switch-checked'
# add_place_on_scheme_button = '.anticon-plus-circle'
add_place_on_scheme_button = '//i[@class="anticon anticon-plus-circle ng-star-inserted"]//ancestor::button[@nz-button]'
location_on_scheme = 'input[formcontrolname="location"]'
location_list_on_scheme = '.ant-select-item'
line_on_scheme = 'input[formcontrolname="line"]'
place_on_scheme = 'input[formcontrolname="place"]'
create_place_button = 'nz-modal-container button[nztype="primary"]'
cancel_place_button = '//span[text()="Отмена"]'