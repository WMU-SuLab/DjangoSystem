# -*- encoding: utf-8 -*-
"""
@File Name      :   download.py    
@Create Time    :   2021/12/7 19:46
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


def download(request):
    page = 'download'
    return render(request, 'SilencerAtlas/download.html', context={
        'title': page,
        'menu': page,
    })
