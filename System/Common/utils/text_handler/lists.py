# -*- encoding: utf-8 -*-
"""
@File Name      :   list.py    
@Create Time    :   2022/2/14 20:48
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'


# 每n个分组
def group_by_step(list_to_group: list, step: int = 10) -> list:
    return [list_to_group[i:i + step] for i in range(0, len(list_to_group), step)]


def group_by_step_yield(list_to_group: list, step: int = 10) -> list:
    for i in range(0, len(list_to_group), step):
        yield list_to_group[i:i + step]


# 分成n个组
def list_to_n_group(list_to_group: list, n: int = 3) -> list:
    length = len(list_to_group)
    remainder = length % n
    if remainder == 0:
        step = length // n
    else:
        step = length // n + 1
    return [list_to_group[i:i + step] for i in range(0, len(list_to_group), step)]


def list_to_n_group_yield(list_to_group: list, n: int = 3) -> list:
    length = len(list_to_group)
    remainder = length % n
    if remainder == 0:
        step = length // n
    else:
        step = length // n + 1
    for i in range(0, len(list_to_group), step):
        yield list_to_group[i:i + step]
