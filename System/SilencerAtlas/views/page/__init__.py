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

from django.urls import path

from .analysis import analysis
from .browse import BrowseView
from .contact import contact
from .download import download
from .genome_browse import genome_browse
from .help import help_page
from .home import home
from .search import search
from .silencer_details import silencer_details
from .statistic import statistics
from .test import test

urlpatterns = [
    path('', home, name='home'),
    path('index',home,name='index'),
    path('test', test, name='test'),
    path('search', search, name='search'),
    path('browse', BrowseView.as_view(), name='browse'),
    path('silencer_details/<str:silencer_id>', silencer_details, name='silencer_details'),
    path('analysis', analysis, name='analysis'),
    path('genome_browse', genome_browse, name='genome_browse'),
    path('statistics', statistics, name='statistics'),
    path('download', download, name='download'),
    path('help', help_page, name='help'),
    path('contact', contact, name='contact'),
]
