# -*- encoding: utf-8 -*-
"""
@File Name      :   snp.py    
@Create Time    :   2022/1/29 18:27
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

from django.views.decorators.http import require_POST

from SilencerAtlas.libs.lists import unknown_value_list
from SilencerAtlas.models.snp import SNP
from utils.response import JsonResponse


@require_POST
def get_snps(request):
    search_text = request.json.get('searchText', '')
    limit = request.json.get('limit', 10)
    page = request.json.get('page', 1)
    snps = SNP.objects.distinct().exclude(rs_id__in=unknown_value_list)
    if search_text:
        snps = snps.filter(rs_id__icontains=search_text)
    count = snps.count()
    if count > page * limit:
        more = True
    else:
        more = False
    rs_ids = list(snps[:limit * page].values_list('rs_id', flat=True))
    return JsonResponse({
        'selects': [{'value': rs_id, 'text': rs_id} for rs_id in rs_ids],
        'more': more,
    })
