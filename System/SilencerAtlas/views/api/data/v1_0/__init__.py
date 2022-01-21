# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/12/7 19:48
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

from .genome_browse import get_igv_reference, get_igv_tracks, get_igv_file_data
from .sample import get_samples, get_sample_by_id, get_sample_silencers_by_id,get_sample_silencers
from .silencer import get_silencers, get_silencer_by_id

urlpatterns = [
    path('get_samples', get_samples, name='get_samples'),
    path('get_sample_by_id/<str:sample_id>', get_sample_by_id, name='get_sample_by_id'),
    path('get_sample_silencers', get_sample_silencers, name='get_sample_silencers'),
    path('get_silencers', get_silencers, name='get_silencers'),
    path('get_silencer_by_id/<str:silencer_id>', get_silencer_by_id, name='get_silencer_by_id'),
    path('get_igv_reference', get_igv_reference, name='get_igv_reference'),
    path('get_igv_tracks', get_igv_tracks, name='get_igv_tracks'),
    path('get_igv_file_data/<path:relative_path>', get_igv_file_data, name='get_igv_file_data')
]
