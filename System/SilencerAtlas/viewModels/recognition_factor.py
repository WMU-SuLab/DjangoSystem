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


def filter_recognition_factors_any(recognition_factors, name):
    for recognition_factor in recognition_factors:
        if recognition_factor.name == name:
            return recognition_factor
