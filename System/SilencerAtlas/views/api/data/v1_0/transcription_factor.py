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

from Common.utils.response import JsonResponse
from SilencerAtlas.models.silencer import SilencerTranscriptionFactor
from SilencerAtlas.viewModels import handle_search_select


@require_POST
def get_transcription_factors(request):
    return JsonResponse(handle_search_select(request.json, SilencerTranscriptionFactor, 'transcription_factor__name'))


@require_POST
def get_silencer_transcription_factor_experiments(request):
    data = request.json
    silencer_id = data.get('silencer_id', None)
    transcription_factor = data.get('transcription_factor', None)
    experiments = SilencerTranscriptionFactor.objects.filter(silencer__silencer_id=silencer_id,
                                                             transcription_factor__name=transcription_factor).first().experiment
    rows = [{'cell_type': experiment.cell_type, 'experiment': experiment.name, } for experiment in experiments]

    return JsonResponse({
        'rows': rows,
    })
