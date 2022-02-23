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

from django.views.decorators.http import require_POST

from SilencerAtlas.models.silencer import SilencerTranscriptionFactor
from SilencerAtlas.viewModels import handle_search_select
from utils.response import JsonResponse


@require_POST
def get_transcription_factors(request):
    return JsonResponse(handle_search_select(request.json, SilencerTranscriptionFactor, 'transcription_factor__name'))
