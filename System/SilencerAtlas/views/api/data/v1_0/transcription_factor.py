# -*- encoding: utf-8 -*-
"""
@File Name      :   transcription_factor.py    
@Create Time    :   2022/1/29 18:28
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
from SilencerAtlas.models.silencer import SilencerTFBs
from django.views.decorators.http import require_POST
from utils.response import JsonResponse


@require_POST
def get_transcription_factors(request):
    search_text = request.json.get('searchText', '')
    limit = request.json.get('limit', 10)
    page = request.json.get('page', 1)
    transcription_factors = SilencerTFBs.objects.distinct().exclude(transcription_factor__name__in=unknown_value_list)
    if search_text:
        transcription_factors = transcription_factors.filter(transcription_factor__name__icontains=search_text)
    count = transcription_factors.count()
    if count > page * limit:
        more = True
    else:
        more = False
    if page == 1:
        transcription_factor_names = list(
            transcription_factors[:page * limit].values_list('transcription_factor__name', flat=True))
    elif page > 1:
        transcription_factor_names = list(
            transcription_factors[(page - 1) * limit: page * limit].values_list('transcription_factor__name',
                                                                                flat=True))
    else:
        transcription_factor_names = []
    return JsonResponse({
        'selects': [{'value': transcription_factor_name, 'text': transcription_factor_name} for
                    transcription_factor_name in transcription_factor_names],
        'more': more,
    })
