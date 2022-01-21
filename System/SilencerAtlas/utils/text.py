# -*- encoding: utf-8 -*-
"""
@File Name      :   text.py    
@Create Time    :   2021/12/31 17:19
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


def text_to_list(text: str):
    return re.sub(r'!|！|；|。|\.|\r\n|\r|\n', ';', text)
