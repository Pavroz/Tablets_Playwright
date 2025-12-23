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

# Загрузка участников
load_button = '.anticon-folder-open'
load_participant_file = os.getcwd() + r'\data\АРМ «ЭЛЕКТРОННЫЕ ТАБЛИЧКИ» Списки участников.csv'

# Таблица с участниками
line_to_participant = 'tbody .ant-table-row'

# Пагинация
pagination_button = '.ant-pagination-item'
prev_page_button = '.ant-pagination-prev'
next_page_button = 'ant-pagination-next'
dropdown_page_button = '.ant-select-selection-item'
page_10_item = '//div[text()="10 / стр."]'
page_20_item = '//div[text()="20 / стр."]'
page_50_item = '//div[text()="50 / стр."]'
page_100_item = '//div[text()="100 / стр."]'

# Поиск
search_field = 'input[placeholder="Поиск"]'
selected_row = 'tr.selected'


sort_button = '//span[text()="Сортировка"]'
checkbox_lastname = '//span[text()=" Фамилия "]//ancestor::label//input[@type="checkbox"]'
checkbox_firstname = '//span[text()=" Имя "]//ancestor::label//input[@type="checkbox"]'
checkbox_middlename = '//span[text()=" Отчество "]//ancestor::label//input[@type="checkbox"]'
checkbox_subject = '//span[text()=" Субъект "]//ancestor::label//input[@type="checkbox"]'
checkbox_position = '//span[text()=" Должность "]//ancestor::label//input[@type="checkbox"]'
checkbox_image = '//span[text()=" Изображение "]//ancestor::label//input[@type="checkbox"]'

# Кнопки возрастания, убывания и очистки
sort_up = '//span[text()="Возрастание"]'
sort_down = '//span[text()="Убывание"]'
cleaning_button = '//span[text()="Очистка"]'

sorting_apply_button = 'nz-modal-container button[nztype="primary"]'