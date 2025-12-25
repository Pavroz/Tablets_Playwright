SORT_CASES = [
    (None, None, None, None, None, None, 'asc'),
    (None, None, None, None, None, None, 'desc'),
    ("lastname", None, None, None, None, None, 'asc'),
    ("lastname", None, None, None, None, None, 'desc'),
    (None, "firstname", None, None, None, None, 'asc'),
    (None, "firstname", None, None, None, None, 'desc'),
    (None, None, "middlename", None, None, None, 'asc'),
    (None, None, "middlename", None, None, None, 'desc'),
    (None, None, None, "subject", None, None, 'asc'),
    (None, None, None, "subject", None, None, 'desc'),
    (None, None, None, None, "position", None, 'asc'),
    (None, None, None, None, "position", None, 'desc'),
    (None, None, None, None, None, "image", 'asc'),
    (None, None, None, None, None, "image", 'desc'),
    ("lastname", "firstname", None, None, None, None, 'asc'),
    ("lastname", "firstname", None, None, None, None, 'desc'),
    ("lastname", "firstname", "middlename", None, None, None, 'asc'),
    ("lastname", "firstname", "middlename", None, None, 'desc', None),
    (None, None, None, "subject", "position", None, 'asc'),
    (None, None, None, "subject", "position", None, 'desc'),
    ("lastname", "firstname", "middlename", "subject", "position", "image", 'asc'),
    ("lastname", "firstname", "middlename", "subject", "position", "image", 'desc'),
]

# BASE_SORT_CASES = [
#     (None, None, None, None, None, None, 'asc'),
#     (None, None, None, None, None, None, 'desc'),
#     ("lastname", None, None, None, None, None, 'asc'),
#     ("lastname", None, None, None, None, None, 'desc'),
#     (None, "firstname", None, None, None, None, 'asc'),
#     (None, "firstname", None, None, None, None, 'desc'),
#     (None, None, "middlename", None, None, None, 'asc'),
#     (None, None, "middlename", None, None, None, 'desc'),
#     (None, None, None, "subject", None, None, 'asc'),
#     (None, None, None, "subject", None, None, 'desc'),
#     (None, None, None, None, "position", None, 'asc'),
#     (None, None, None, None, "position", None, 'desc'),
#     (None, None, None, None, None, "image", 'asc'),
#     (None, None, None, None, None, "image", 'desc'),
#     ("lastname", "firstname", None, None, None, None, 'asc'),
#     ("lastname", "firstname", None, None, None, None, 'desc'),
#     ("lastname", "firstname", "middlename", None, None, None, 'asc'),
#     ("lastname", "firstname", "middlename", None, None, 'desc', None),
#     (None, None, None, "subject", "position", None, 'asc'),
#     (None, None, None, "subject", "position", None, 'desc'),
#     ("lastname", "firstname", "middlename", "subject", "position", "image", 'asc'),
#     ("lastname", "firstname", "middlename", "subject", "position", "image", 'desc'),
# ]
#
# DIRECTIONS = ["asc", "desc"]
#
# # Генерация 22 кортежей с последним параметром direction
# SORT_CASES = [
#     (*case, direction)
#     for case in BASE_SORT_CASES
#     for direction in DIRECTIONS
# ]
#
# # Проверка длины
# assert len(SORT_CASES) == 22