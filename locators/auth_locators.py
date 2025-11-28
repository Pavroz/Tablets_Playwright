login = 'input[formcontrolname="login"]'
password = 'input[formcontrolname="password"]'
recovery_conf_active = '.ant-switch-checked'
auth_button = '.login-form-button'
notification = 'div.ant-notification-notice'

# Валидация при пустых полях ввода
# login_validation = 'nz-form-control[nzerrortip="Пожалуйста, введите логин!"]'
# password_validation = 'nz-form-control[nzerrortip="Пожалуйста, введите пароль!"]'
login_validation = '(//div[@role="alert"])[1]'
password_validation = '(//div[@role="alert"])[2]'
