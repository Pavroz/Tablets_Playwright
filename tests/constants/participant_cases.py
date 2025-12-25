CREATE_PARTICIPANT_CASES = [
            (None, None, None, None),  # только обязательные поля
            ("middlename", None, None, None),  # + отчество
            (None, "subject", None, None),  # + субъект
            (None, None, "position", None),  # + должность
            (None, None, None, "image"),  # + изображение
            ("middlename", "subject", "position", "image"),  # всё вместе
        ]