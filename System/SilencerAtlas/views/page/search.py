# -*- encoding: utf-8 -*-
"""
@File Name      :   search.py    
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
from django.views.decorators.cache import cache_page

from SilencerAtlas.libs.model_choices import sources, species, bio_sample_types, strategies, variants
# from SilencerAtlas.libs.lists import unknown_value_list
# from SilencerAtlas.models.gene import Gene
# from SilencerAtlas.models.sample import Sample
# from SilencerAtlas.models.silencer import SilencerTranscriptionFactor
# from SilencerAtlas.models.snp import SNP


@cache_page(60 * 60 * 24 * 10)
def search(request):
    page = 'search'
    # tissue_types = list(Sample.objects.distinct().exclude(tissue_type__in=unknown_value_list)[:20].values_list('tissue_type', flat=True))
    # genes = list(Gene.objects.distinct().exclude(name__in=unknown_value_list,region=None)[:20].values_list('name', flat=True))
    # transcription_factors = list(SilencerTFBs.objects.distinct().exclude(transcription_factor__name__in=unknown_value_list)[:20].values_list('transcription_factor__name', flat=True))
    # rs_ids = list(SNP.objects.distinct().exclude(rs_id__in=unknown_value_list)[:20].values_list('rs_id', flat=True))
    return render(request, 'SilencerAtlas/search.html', context={
        'title': page,
        'menu': page,
        # 字典
        'sources': sources.items(),
        'species': species.items(),
        'bio_sample_types': bio_sample_types.items(),
        # 'tissue_types': tissue_types,
        # 'genes': genes,
        'strategies': strategies.items(),
        # 'transcription_factors': transcription_factors,
        # 'rs_ids': rs_ids,
        'variants': variants.items(),
    })
