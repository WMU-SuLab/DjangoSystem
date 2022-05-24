# -*- encoding: utf-8 -*-
"""
@File Name      :   recognition_factor.py    
@Create Time    :   2022/1/23 21:44
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

import re

from Common.utils.text_handler import upper_text


def to_recognition_factors_dict(recognition_factors):
    return {recognition_factor.name: recognition_factor for recognition_factor in recognition_factors}


def filter_recognition_factors_any(recognition_factors, name):
    for recognition_factor in recognition_factors:
        if recognition_factor.name == name:
            return recognition_factor


def recognition_factors_upper(recognition_factor: str):
    return upper_text(recognition_factor, 'hk')


def recognition_factors_lower(recognition_factor: str):
    return recognition_factor.lower()


def recognition_factors_to_list(recognition_factors: str):
    if 'only' in recognition_factors:
        return recognition_factors.split(' ')[0]
    elif 'not' in recognition_factors:
        return ''
    else:
        return re.sub(' ', '', re.sub('[&,，；]', ';', recognition_factors))
