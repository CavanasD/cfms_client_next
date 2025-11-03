from enum import Enum

__all__ = ["SortMode", "SortOrder"]


class SortMode(Enum):
    BY_NAME = 0
    BY_CREATED_AT = 1
    BY_LAST_MODIFIED = 2
    BY_SIZE = 3
    BY_TYPE = 4
    

class SortOrder(Enum):
    ASCENDING = 0
    DESCENDING = 1