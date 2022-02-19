# -*- encoding: utf-8 -*-
"""
@File Name      :   sample.py    
@Create Time    :   2021/12/28 19:35
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

import json

from django.db.models import Q, F
from django.views.decorators.http import require_POST, require_GET
from django_mysql.models import GroupConcat

from SilencerAtlas.models.sample import Sample
from SilencerAtlas.models.silencer import Silencer
from SilencerAtlas.viewModels import handle_search_select, handle_sort_order, handle_pagination
from SilencerAtlas.viewModels.silencer import filtered_sample_chosen_silencers
from utils.response import JsonResponse


@require_POST
def get_bio_sample_names(request):
    return JsonResponse(handle_search_select(request.json, Sample, 'bio_sample_name'))


@require_POST
def get_tissue_types(request):
    return JsonResponse(handle_search_select(request.json, Sample, 'tissue_type'))


@require_GET
def get_sample_by_id(request, sample_id):
    sample = Sample.objects.get(id=sample_id)
    return JsonResponse(
        {sample.to_dict(fields=['sample_id', 'bio_sample_name', 'bio_sample_type', 'species', 'source'])})


@require_POST
def get_sample_silencers(request):
    data: dict = request.json
    print(data)
    silencers = filtered_sample_chosen_silencers(data)
    # 构建表格属性
    silencers = silencers.annotate(
        chromosome=F('region__chromosome'),
        start=F('region__start'),
        end=F('region__end'),
        recognition_factors_group_concat=GroupConcat(
            'silencerrecognitionfactors__recognition_factor__name', distinct=True),
        species=F('sample__species'),
        # tissue_type=F('sample__tissue_type'),
        bio_sample_type=F('sample__bio_sample_type'),
        bio_sample_name=F('sample__bio_sample_name'),
    )
    # 先查询
    # 由于插件问题传过来的是字符串，需要转换成字典
    filters = data.get('filters', '')
    if filters:
        filters = json.loads(filters)
        silencer_id = filters.get('silencer_id', '')
        if silencer_id:
            silencers = silencers.filter(silencer_id__icontains=silencer_id)
        loci = filters.get('loci', '')
        chromosome, start_end = loci.split(':')
        start, end = start_end.split('-')
        if chromosome:
            silencers = silencers.filter(chromosome__icontains=chromosome)
        if start:
            silencers = silencers.filter(start__icontains=start)
        if end:
            silencers = silencers.filter(end__icontains=end)
        recognition_factors_group_concat = filters.get('recognition_factors', '')
        if recognition_factors_group_concat:
            silencers = silencers.filter(
                recognition_factors_group_concat__icontains=recognition_factors_group_concat)
        species = filters.get('species', '')
        if species:
            silencers = silencers.filter(species__icontains=species)
        # tissue_type = filters.get('tissue_type', '')
        # if tissue_type:
        #     silencers = silencers.filter(tissue_type__icontains=tissue_type)
        bio_sample_type = filters.get('bio_sample_type', '')
        if bio_sample_type:
            silencers = silencers.filter(bio_sample_type__icontains=bio_sample_type)
        bio_sample_name = filters.get('bio_sample_name', '')
        if bio_sample_name:
            silencers = silencers.filter(bio_sample_name__icontains=bio_sample_name)
    # 综合查询拥有更高的权限
    search_text = data.get('searchText', '')
    if search_text:
        silencers = silencers.filter(
            Q(silencer_id__icontains=search_text) | Q(chromosome__icontains=search_text) |
            Q(start__icontains=search_text) | Q(start__icontains=search_text) |
            Q(recognition_factors_group_concat__icontains=search_text) | Q(species__icontains=search_text) |
            # Q(tissue_type__icontains=search_text) |
            Q(bio_sample_type__icontains=search_text) | Q(bio_sample_name__icontains=search_text)
        )
    # 再排序
    silencers = handle_sort_order(data, silencers)
    # 再分页
    silencers_current_page, total, first_load = handle_pagination(data, Silencer, silencers)
    rows = [{
        'id': silencer.id,
        'silencer_id': silencer.silencer_id,
        'loci': silencer.region.loci if silencer.region else '',
        'species': silencer.sample.species if silencer.sample else '',
        'bio_sample_type': silencer.sample.bio_sample_type if silencer.sample else '',
        # 'tissue_cell_type': silencer.sample.tissue_cell_type if silencer.sample else '',
        'bio_sample_name': silencer.sample.bio_sample_name if silencer.sample else '',
        'recognition_factors': silencer.recognition_factors_group_concat or 'null',
    } for silencer in silencers_current_page]
    return JsonResponse({
        'total': total,
        'rows': rows,
        'firstLoad': first_load,
    })


@require_GET
def get_sample_silencers_by_id(request, sample_id):
    sample = Sample.objects.get(id=sample_id)
    silencers = sample.silencers
    total = silencers.count()
    return JsonResponse({
        'total': total,
        'rows': [silencer.to_dict(fields=['silencer_id', 'chr', 'start', 'end', 'length', 'score', 'strand']) for
                 silencer in silencers]
    })
