# -*- encoding: utf-8 -*-
"""
@File Name      :   lists.py    
@Create Time    :   2021/10/17 18:16
@Description    :   
@Version        :   
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
@other information
"""
__auth__ = "diklios"

from .model_choices import recognition_factors, unknown

igv_colors = [
    'rgb(215,25,28)', 'rgb(253,174,97)', 'rgb(171,217,233)', 'rgb(44,123,182)', '#fff566',
    "#389e0d", "#08979c", "#722ed1", "#ff441a", "#a3b61f", "#75856d", "#c78738", "#cc0000",
]
unknown_value_list = list(unknown.keys())
recognition_factors_value_list = recognition_factors.keys()
