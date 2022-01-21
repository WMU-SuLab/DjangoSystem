# -*- encoding: utf-8 -*-
"""
@File Name      :   test.py    
@Create Time    :   2021/12/29 20:00
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
from django.http import JsonResponse
from SilencerAtlas.models.sample import Sample

def test(request):
    samples=Sample.objects.all().values('tissue_type').distinct().exclude(
        tissue_type__in=['', 'unknown'])
    for sample in samples:
        print(sample)

    return JsonResponse({'test':'success','data':[]})