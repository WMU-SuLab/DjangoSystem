# -*- encoding: utf-8 -*-
"""
@File Name      :   genome_browse.py    
@Create Time    :   2021/12/7 19:45
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

from SilencerAtlas.libs.dicts import genome_tree_data


@cache_page(60 * 60 * 24)
def genome_browse(request):
    page = 'genome_browse'
    return render(request, 'SilencerAtlas/genome_browse.html', context={
        'title': page,
        'menu': page,
        'genome_tree_data': genome_tree_data,
        'tracks': [],
    })
