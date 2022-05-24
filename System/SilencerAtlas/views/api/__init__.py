# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/12/7 18:58
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

from django.urls import path, include

from SilencerAtlas import app_name
from .test import test

urlpatterns = [
    path('test', test, name='test'),
    path('data/', include(('SilencerAtlas.views.api.data', app_name), namespace='data')),
    path('utils/', include(('SilencerAtlas.views.api.utils', app_name), namespace='utils')),
]
