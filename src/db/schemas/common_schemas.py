from enum import Enum


class Role(int, Enum):
    ADMIN = 1
    EDITOR = 2
    ACCOUNT_MANAGER = 3
    JOURNALIST = 4
