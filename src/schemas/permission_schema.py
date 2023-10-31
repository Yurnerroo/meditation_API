from enum import Enum


class UserPermissions(int, Enum):
    READ: int = 1
    UPDATE: int = 2
    DELETE: int = 3
    CREATE: int = 4


class GroupPermissions(int, Enum):
    READ: int = 5
    UPDATE: int = 6
    DELETE: int = 7
    CREATE: int = 8


class Permissions(int, Enum):
    READ: int = 9
    UPDATE: int = 10
    DELETE: int = 11
    CREATE: int = 12


class UsersGroupsPermissions(int, Enum):
    READ: int = 13
    UPDATE: int = 14
    DELETE: int = 15
    CREATE: int = 16


class GroupsPermissionsPermissions(int, Enum):
    READ: int = 17
    UPDATE: int = 18
    DELETE: int = 19
    CREATE: int = 20


class CategoryPermissions(int, Enum):
    READ: int = 21
    UPDATE: int = 22
    DELETE: int = 23
    CREATE: int = 24


class MatchPermissions(int, Enum):
    READ: int = 25
    UPDATE: int = 26
    DELETE: int = 27
    CREATE: int = 28


class RatingPermissions(int, Enum):
    READ: int = 29
    UPDATE: int = 30
    DELETE: int = 31
    CREATE: int = 32
