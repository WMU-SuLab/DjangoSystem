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
from django_mysql.models import GroupConcat

from SilencerAtlas.models.silencer import Silencer
from SilencerAtlas.viewModels.recognition_factor import recognition_factors_upper


@require_GET
def silencer_details(request, silencer_id):
    page = 'silencer_details'

    silencer = Silencer.objects.annotate(
        recognition_factors_group_concat=GroupConcat(
            'silencerrecognitionfactor__recognition_factor__name', distinct=True),
    ).prefetch_related('sample','region').get(id=silencer_id)
    # 这里的sample和region其实可以优化为查询一次数据库，但是这样就要在一次查询中使用concat()拼接或者silencer对象中手动拼接字符串了，考虑到只有一个对象要查，就还可以接受
    details = {
        'silencer_id': silencer.silencer_id,
        'species': silencer.sample.species if silencer.sample else '',
        'source': silencer.sample.source if silencer.sample else '',
        'bio_sample_type': silencer.sample.bio_sample_type if silencer.sample else '',
        # 'tissue_type': silencer.sample.tissue_type if silencer.sample else '',
        'bio_sample_name': silencer.sample.bio_sample_name if silencer.sample else '',
        'genomic_loci': silencer.region.loci if silencer.region else '',
        'size': silencer.region.size if silencer.region else '',
        'recognition_factors': recognition_factors_upper(silencer.recognition_factors_group_concat or '--'),
    }
    return render(request, 'SilencerAtlas/silencer_details.html', context={
        'title': page,
        'menu': page,
        'silencer': details,
    })