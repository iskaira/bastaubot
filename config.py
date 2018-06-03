# -*- coding: utf-8 -*-

from enum import Enum

db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    kirispe_pikir = "1"
    syltaular = "2"
    kadam_1_pikir = "3"
    kadam_3_pikir = "4"
    kadam_4_pikir = "5"
    kadam_5_pikir = "6"
    korytyndy = "7"
