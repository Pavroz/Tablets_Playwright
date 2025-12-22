import logging



def get_logger(name: str) -> logging.Logger:
    """
        Создаёт и возвращает логгер с заданным именем.

        Логгер:
        - Устанавливает уровень логирования DEBUG
        - Выводит логи в консоль (stdout)
        - Использует формат: "дата | имя логгера | уровень | сообщение"

        :param name: Имя логгера (обычно имя модуля или класса)
        :return: Конфигурированный logging.Logger
        """
    logger = logging.getLogger(name) # Создаем логгер с указаннм именем
    logger.setLevel(logging.DEBUG) # Устанавливаем уровень логирования DEBUG

    handler = logging.StreamHandler() # Создаем обработчик, который пишет в stdout
    handler.setLevel(logging.DEBUG) # Тоже уровень DEBUG

    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    ) # Формат логов: время | имя логгера | уровень | сообщение

    handler.setFormatter(formatter) # Применяем формат к обработчику
    logger.addHandler(handler) # Добавляем обработчик к логгеру

    return logger # Возвращаем готовый логгер


# Пример логгирования в коде
#
# from tools.logger import get_logger
# logger = get_logger("NAME_OF_MY_LOGGER")
#
# logger.info("Открываем страницу регистрации")
# logger.debug("Вводим email test@example.com")
# logger.error("Не удалось найти кнопку 'Submit'")