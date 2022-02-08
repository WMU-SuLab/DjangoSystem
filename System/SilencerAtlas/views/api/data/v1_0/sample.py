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
from SilencerAtlas.libs.lists import unknown_value_list
from SilencerAtlas.models.sample import Sample
from SilencerAtlas.viewModels.silencer import filtered_sample_chosen_silencers
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.views.decorators.http import require_POST, require_GET
from django_mysql.models import GroupConcat
from utils.response import JsonResponse


@require_POST
def get_tissue_types(request):
    search_text = request.json.get('searchText', '')
    limit = request.json.get('limit', 10)
    page = request.json.get('page', 1)
    samples = Sample.objects.distinct().exclude(tissue_type__in=unknown_value_list)
    if search_text:
        samples = samples.filter(tissue_type__icontains=search_text)
    count = samples.count()
    if count > page * limit:
        more = True
    else:
        more = False
    if page == 1:
        tissue_types = list(samples[:page * limit].values_list('tissue_type', flat=True))
    elif page > 1:
        tissue_types = list(samples[(page - 1) * limit:page * limit].values_list('tissue_type', flat=True))
    else:
        tissue_types = []
    return JsonResponse({
        'selects': [{'value': tissue_type, 'text': tissue_type} for tissue_type in tissue_types],
        'more': more,
    })


@require_POST
def get_samples(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    # bio_sample_names_chosen = lower_underline_list(data.get('bioSamplesNamesChosen', []))
    bio_sample_names_chosen = data.get('bioSamplesNamesChosen', [])
    if not bio_sample_names_chosen:
        samples = Sample.objects.all()
    else:
        samples = Sample.objects.filter(bio_sample_name__in=bio_sample_names_chosen)
    # 排除unknown的数据
    samples = samples.exclude(Q(sample_id='unknown') | Q(bio_sample_name='unknown') | Q(bio_sample_type='unknown') |
                              Q(tissue_type='unknown') | Q(species='unknown') | Q(source='unknown'))
    # # 表格操作
    # search_text = data.get('searchText', '')
    # order_name = data.get('orderName', None)
    # sort_order = data.get('sortOrder', None)
    # page_size = data.get('pageSize', 20)
    # current_page = data.get('currentPage', 1)
    # # 是否查询
    # if search_text != '':
    #     samples = samples.filter(Q(sample_id__icontains=search_text) | Q(bio_sample_name__icontains=search_text) |
    #                              Q(bio_sample_type__icontains=search_text) | Q(tissue_type__icontains=search_text) |
    #                              Q(species__icontains=search_text) | Q(source__icontains=search_text))
    # # 是否排序
    # # 默认根据sample_id排序
    # samples.order_by('sample_id')
    # if order_name:
    #     if sort_order in ['asc', 'ascending']:
    #         samples = samples.order_by(order_name)
    #     elif sort_order in ['desc', 'descending']:
    #         samples = samples.order_by(*{'-' + order_name})
    # # 分页
    # # 需要限制数量
    # samples_paginator = Paginator(samples[:1000], page_size)
    # total = samples_paginator.count
    # samples_current_page = samples_paginator.get_page(current_page)
    # table_rows = [sample.to_dict(
    #     fields=['id', 'sample_id', 'bio_sample_name', 'tissue_type', 'bio_sample_type', 'species', 'source'])
    #     for sample in samples_current_page]

    # 在执行查询时选择silencer的数据
    samples.select_related('silencers')
    print(len(samples))
    total = 0
    table_rows = []
    for sample in samples:
        for silencer in sample.silencers.all():
            silencer_modifications = silencer.silencermodification_set.all()
            total += len(silencer_modifications)
            row = silencer.to_dict(fields=['id', 'silencer_id'])
            row['species'] = silencer.sample.species
            row['recognition_factor'] = ''
            for silencer_modification in silencer_modifications:
                if silencer_modification.recognition_factor:
                    row['recognition_factor'] += silencer_modification.modification.name
            row['loci'] = silencer.chromosome + ":" + str(silencer.start) + "-" + str(silencer.end)
            row['bio_sample_name'] = sample.bio_sample_name
            row['tissue_cell_type'] = sample.tissue_type
            row['bio_sample_type'] = sample.bio_sample_type
            table_rows.append(row)
    return JsonResponse({'code': 1, 'msg': 'success', 'data': {'total': total, 'rows': table_rows}})


@require_GET
def get_sample_by_id(request, sample_id):
    sample = Sample.objects.get(id=sample_id)
    return JsonResponse({'code': 1, 'msg': 'success', 'data': sample.to_dict(
        fields=['sample_id', 'bio_sample_name', 'tissue_type', 'bio_sample_type', 'species', 'source'])})


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
        tissue_type=F('sample__tissue_type'),
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
        tissue_type = filters.get('tissue_type', '')
        if tissue_type:
            silencers = silencers.filter(tissue_type__icontains=tissue_type)
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
            Q(tissue_type__icontains=search_text) | Q(bio_sample_type__icontains=search_text) |
            Q(bio_sample_name__icontains=search_text)
        )
    # 再排序
    multi_sort = data.get('multiSort', [])
    if multi_sort:
        for sort in multi_sort:
            order_name = sort.get('orderName', '')
            sort_order = sort.get('sortOrder', '')
            if order_name:
                if sort_order in ['asc', 'ascending']:
                    silencers = silencers.order_by(order_name)
                elif sort_order in ['desc', 'descending']:
                    silencers = silencers.order_by(*{'-' + order_name})
    # 表格中的单个排序拥有更高的权限
    order_name = data.get('orderName', '')
    sort_order = data.get('sortOrder', '')
    if order_name:
        if sort_order in ['asc', 'ascending']:
            silencers = silencers.order_by(order_name)
        elif sort_order in ['desc', 'descending']:
            silencers = silencers.order_by(*{'-' + order_name})
    # 再分页
    silencers = silencers.prefetch_related('region', 'sample')
    page_size = data.get('pageSize', 10)
    current_page = data.get('currentPage', 1)
    silencers_paginator = Paginator(silencers, page_size)
    total = silencers_paginator.count
    silencers_current_page = silencers_paginator.get_page(current_page)
    rows = [{
        'id': silencer.id,
        'silencer_id': silencer.silencer_id,
        'loci': silencer.region.loci,
        'species': silencer.sample.species,
        'bio_sample_type': silencer.sample.bio_sample_type,
        'tissue_cell_type': silencer.sample.tissue_cell_type,
        'bio_sample_name': silencer.sample.bio_sample_name,
        'recognition_factors': silencer.recognition_factors_group_concat or 'null',
    } for silencer in silencers_current_page]
    return JsonResponse({
        'total': total,
        'rows': rows,
    })


@require_GET
def get_sample_silencers_by_id(request, sample_id):
    sample = Sample.objects.get(id=sample_id)
    silencers = sample.silencers
    total = len(silencers)
    return JsonResponse({'code': 1, 'msg': 'success', 'data': {
        'total': total,
        'rows': [silencer.to_dict(
            fields=['id', 'silencer_id', 'chr', 'start', 'end', 'length', 'score', 'strand', 'gene_symbol', 'TF',
                    'CRISPR'])
            for silencer in silencers]}})
