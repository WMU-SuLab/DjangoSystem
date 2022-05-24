# -*- encoding: utf-8 -*-
"""
@File Name      :   home.py    
@Create Time    :   2021/12/7 19:20
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

from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(60 * 60 * 24)
def home(request):
    page = 'home'
    return render(request, 'SilencerAtlas/home.html', context={'title': page, 'menu': page})
