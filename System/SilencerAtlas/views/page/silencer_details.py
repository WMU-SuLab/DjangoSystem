# -*- encoding: utf-8 -*-
"""
@File Name      :   silencer.py    
@Create Time    :   2021/12/7 19:44
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
from django.views.decorators.http import require_GET
from django.db.models import Q
from django_mysql.models import GroupConcat

from SilencerAtlas.models.silencer import Silencer

from SilencerAtlas.libs.lists import recognition_factors_value_list

@require_GET
def silencer_details(request, silencer_id):
    page = 'silencer_details'

    silencer = Silencer.objects.annotate(
        recognition_factors_group_concat=GroupConcat(
            'silencerrecognitionfactors__recognition_factor__name', distinct=True),
    ).prefetch_related('sample','region').get(id=silencer_id)
    # 这里的sample和region其实可以优化为查询一次数据库，但是这样就要在一次查询中使用concat()拼接或者silencer对象中手动拼接字符串了，考虑到只有一个对象要查，就还可以接受
    details = {
        'silencer_id': silencer.silencer_id,
        'species': silencer.sample.species,
        'source': silencer.sample.source,
        'bio_sample_type': silencer.sample.bio_sample_type,
        'tissue_type': silencer.sample.tissue_type,
        'bio_sample_name': silencer.sample.bio_sample_name,
        'genomic_loci': silencer.region.loci,
        'size': silencer.region.size,
        'recognition_factors': silencer.recognition_factors_group_concat,
        'normalized_signal': '',
    }
    return render(request, 'SilencerAtlas/silencer_details.html', context={
        'title': page,
        'menu': page,
        'silencer': details,
    })