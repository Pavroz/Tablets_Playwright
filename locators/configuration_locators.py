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
schemes_selector = '.ant-select-selector'
schemes_dropdown = '.ant-select-dropdown'
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