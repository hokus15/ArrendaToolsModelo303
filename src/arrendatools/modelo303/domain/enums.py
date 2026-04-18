from enum import Enum


class Period(str, Enum):
    FIRST_QUARTER = "1T"
    SECOND_QUARTER = "2T"
    THIRD_QUARTER = "3T"
    FOURTH_QUARTER = "4T"
