SORT_CASES = [
    (None, None, None, None, None, None),
    ("lastname", None, None, None, None, None),
    (None, "firstname", None, None, None, None),
    (None, None, "middlename", None, None, None),
    (None, None, None, "subject", None, None),
    (None, None, None, None, "position", None),
    (None, None, None, None, None, "image"),
    ("lastname", "firstname", None, None, None, None),
    ("lastname", "firstname", "middlename", None, None, None),
    (None, None, None, "subject", "position", None),
    ("lastname", "firstname", "middlename", "subject", "position", "image"),
]