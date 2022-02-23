# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/12/31 17:14
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

from typing import Type

from django.conf import settings
from django.db.models import Model

from SilencerAtlas.libs.lists import unknown_value_list
from SilencerAtlas.models.base import Base


def handle_search_select(data: dict, model: Type[Base]|Type[Model], field: str):
    search_text = data.get('searchText', '')
    limit = data.get('limit', 10)
    page = data.get('page', 1)
    rows = model.objects.exclude(**{field + '__in': unknown_value_list})
    if search_text:
        rows = rows.filter(**{field + '__icontains': search_text})
    count = rows.count()
    if count > page * limit:
        more = True
    else:
        more = False
    if page == 1:
        fields = list(set(rows[:page * limit].values_list(field, flat=True)))
    elif page > 1:
        fields = list(set(rows[(page - 1) * limit:page * limit].values_list(field, flat=True)))
    else:
        fields = []
    return {'selects': [{'value': field_item, 'text': field_item} for field_item in fields], 'more': more}


def handle_pagination(data: dict, model: Type[Base]|Type[Model], rows):
    total = data.get('total', 0)
    first_load = data.get('firstLoad', False)
    page_size = data.get('pageSize', 10)
    current_page = data.get('currentPage', 1)
    # rows_paginator = Paginator(rows, page_size)
    # total = rows_paginator.count
    # rows_current_page = rows_paginator.get_page(current_page)
    if first_load:
        total = model.objects.values('id').count()
        first_load = False
    else:
        if current_page == 1:
            total = rows.values('id').count()
    total = total if total <= settings.MODEL_TOTAL_LIMIT else settings.MODEL_TOTAL_LIMIT
    rows_current_page = rows[(current_page - 1) * page_size:current_page * page_size]
    return rows_current_page, total, first_load


def sort_rows(data: dict, rows):
    order_name = data.get('orderName', '')
    sort_order = data.get('sortOrder', '')
    if order_name:
        if sort_order in ['asc', 'ascending']:
            rows = rows.order_by(order_name)
        elif sort_order in ['desc', 'descending']:
            rows = rows.order_by(*{'-' + order_name})
    return rows


def handle_sort_order(data: dict, rows):
    multi_sort = data.get('multiSort', [])
    if multi_sort:
        for sort in multi_sort:
            rows = sort_rows(sort, rows)
    # 表格中的单个排序拥有更高的权限
    rows = sort_rows(data, rows)
    return rows
