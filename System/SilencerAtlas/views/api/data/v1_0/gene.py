# -*- encoding: utf-8 -*-
"""
@File Name      :   gene.py    
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

from SilencerAtlas.libs.lists import unknown_value_list
from SilencerAtlas.models.gene import Gene
from django.views.decorators.http import require_POST
from utils.response import JsonResponse


@require_POST
def get_genes(request):
    search_text = request.json.get('searchText', '')
    limit = request.json.get('limit', 10)
    page = request.json.get('page', 1)
    genes = Gene.objects.distinct().exclude(name__in=unknown_value_list)
    if search_text:
        genes = genes.filter(name__icontains=search_text)
    count = genes.count()
    if count > page * limit:
        more = True
    else:
        more = False
    if page == 1:
        names = list(genes[:page * limit].values_list('name', flat=True))
    elif page > 1:
        names = list(genes[(page - 1) * limit:page * limit].values_list('name', flat=True))
    else:
        names = []
    return JsonResponse({
        'selects': [{'value': name, 'text': name} for name in names],
        'more': more,
    })
