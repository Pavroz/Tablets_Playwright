import os

# Создание, удаление и редактирование участника
create_button = '.anticon.anticon-plus'
edit_button = '.anticon.anticon-edit'

# Модалка создания/редактирования участника
lastname_field = 'input[formcontrolname="lastName"]'
firstname_field = 'input[formcontrolname="firstName"]'
middlename_field = 'input[formcontrolname="middleName"]'
subject_field = 'input[formcontrolname="county"]'
position_field = 'input[formcontrolname="position"]'
add_image_button = '.image-drag input[type="file"]'

# Кнопки создания и отмены
create_button_in_modal = '//span[text()="Создать "]'
save_button_in_modal = '//span[text()="Сохранить "]'
cancel_button_in_modal = '//span[text()="Отмена"]'
cross_button_in_modal = '.ant-modal-close-x'

# Удаление участника
delete_button = '.anticon.anticon-delete'
apply_delete_button = 'button[cdkfocusinitial="true"]'

# Взаимодействие с изображением
file_path = os.getcwd() + r'\data\image.png'
view_image_button = '//span[text()="Просмотр изображения"]'
no_image_notification = '//div[text()="Для участника не загружено изображение!"]'
modal_with_image = 'div.ant-modal-body img'
button_is_disable = '//button[@disabled="true"]//span[text()="Просмотр изображения"]'
modal_close_button = '.ant-modal-close-x'