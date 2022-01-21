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
from .model_choices import recognition_factors
igv_colors = ['rgb(215,25,28)', 'rgb(253,174,97)', 'rgb(171,217,233)', 'rgb(44,123,182)']
unknown_value_list = ['', 'unknown']
recognition_factors_value_list=recognition_factors.keys()-unknown_value_list
