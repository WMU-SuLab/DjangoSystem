# -*- encoding: utf-8 -*-
"""
@File Name      :   browse.py    
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
import time
from django.shortcuts import render
from django.views.generic import TemplateView

from SilencerAtlas.libs.lists import unknown_value_list
from SilencerAtlas.libs.model_choices import sources, species, bio_sample_types
from SilencerAtlas.models.sample import Sample
from SilencerAtlas.models.silencer import Silencer
from SilencerAtlas.viewModels.silencer import silencers_classify_count, \
    silencers_classify_count_filter_zero, filtered_sample_chosen_silencers
from utils.response import JsonResponse


class BrowseView(TemplateView):
    template_name = 'SilencerAtlas/browse.html'
    page = 'browse'
    context = {
        # 页面
        'title': page,
        'menu': page,
    }

    def handle_count(self, silencers):
        all_silencers_count = silencers.count()
        sources_silencers_count = silencers_classify_count('source', sources, have_silencers=True, silencers=silencers)
        species_silencers_count = silencers_classify_count('species', species, have_silencers=True, silencers=silencers)
        bio_sample_types_silencers_count = silencers_classify_count('bio_sample_type', bio_sample_types,
                                                                    have_silencers=True, silencers=silencers)
        # tissue_types = list(Sample.objects.values_list('tissue_type', flat=True).distinct().exclude(
        #     tissue_type__in=unknown_value_list))
        # tissue_types_select_data = silencers_classify_count_filter_zero(
        #     'tissue_type', {tissue_type: tissue_type for tissue_type in tissue_types}, have_silencers=True, silencers=silencers)
        bio_sample_names = list(Sample.objects.values_list('bio_sample_name', flat=True).distinct().exclude(
            bio_sample_name__in=unknown_value_list))
        bio_sample_names_select_data = silencers_classify_count_filter_zero(
            'bio_sample_name', {bio_sample_name: bio_sample_name for bio_sample_name in bio_sample_names},
            have_silencers=True, silencers=silencers)
        print({
            **self.context,
            'allSilencersCount': all_silencers_count,
            'sourcesSilencersCount': sources_silencers_count,
            'speciesSilencersCount': species_silencers_count,
            'bioSampleTypesSilencersCount': bio_sample_types_silencers_count,
            # 'tissueTypesSelectData': tissue_types_select_data,
            'bioSampleNamesSelectData': bio_sample_names_select_data,
        })
        return {
            **self.context,
            'allSilencersCount': all_silencers_count,
            'sourcesSilencersCount': sources_silencers_count,
            'speciesSilencersCount': species_silencers_count,
            'bioSampleTypesSilencersCount': bio_sample_types_silencers_count,
            # 'tissueTypesSelectData': tissue_types_select_data,
            'bioSampleNamesSelectData': bio_sample_names_select_data,
        }

    def get(self, request, *args, **kwargs):
        # silencers = filtered_unknown_silencers()
        silencers = Silencer.objects.all()
        return render(request, template_name=self.template_name, context=self.handle_count(silencers))

    def post(self, request, *args, **kwargs):
        data: dict = request.json
        print(data)
        silencers = filtered_sample_chosen_silencers(data)
        return JsonResponse(self.handle_count(silencers))
