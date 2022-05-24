# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/12/1 14:19
@Description    :   
@Version        :   
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'


def lower_underline(text: str) -> str:
    """
    :params text:一般的带空格的英文
    :return:小写+下划线的英文
    """
    if not isinstance(text, str):
        raise TypeError('text must be str')
    return text.strip().lower().replace(' ', '_')


def lower_underline_list(text_list: list) -> list:
    return [lower_underline(item) for item in text_list]


def lower_text(text: str, upper: str, ) -> str:
    """
    :params upper_text:需要转换的字符串
    :params lower_text:转换后的字符串
    :return:
    """
    lower_map = str.maketrans(upper, upper.lower())
    return text.translate(lower_map)


def upper_text(text: str, lower: str) -> str:
    """
    :params lower_text:需要转换的字符串
    :params upper_text:转换后的字符串
    :return:
    """
    upper_map = str.maketrans(lower, lower.upper())
    return text.translate(upper_map)
