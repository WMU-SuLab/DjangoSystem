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

from django.shortcuts import render
from django.views.generic import TemplateView

from SilencerAtlas.libs.lists import unknown_value_list
from SilencerAtlas.libs.model_choices import sources, species, bio_sample_types
from SilencerAtlas.models.sample import Sample
from SilencerAtlas.viewModels.silencer import filtered_unknown_silencers, silencers_classify_count, \
    silencers_classify_count_filter_zero
from utils.response import JsonResponse


class BrowseView(TemplateView):
    template_name = 'SilencerAtlas/browse.html'
    page = 'browse'
    context = {
        # 页面
        'title': page,
        'menu': page,
    }

    def get(self, request, *args, **kwargs):
        all_silencers_count = filtered_unknown_silencers().count()
        sources_silencers_count = silencers_classify_count('source', sources)
        species_silencers_count = silencers_classify_count('species', species)
        bio_sample_types_silencers_count = silencers_classify_count('bio_sample_type', bio_sample_types)
        tissue_types = list(Sample.objects.values_list('tissue_type', flat=True).distinct().exclude(
            tissue_type__in=unknown_value_list))
        tissue_types_select_data = silencers_classify_count_filter_zero('tissue_type',
                                                                        {tissue_type: tissue_type for tissue_type in
                                                                         tissue_types})
        bio_sample_names = list(Sample.objects.values_list('bio_sample_name', flat=True).distinct().exclude(
            bio_sample_name__in=unknown_value_list))
        bio_sample_names_select_data = silencers_classify_count_filter_zero('bio_sample_name',
                                                                            {bio_sample_name: bio_sample_name for
                                                                             bio_sample_name in bio_sample_names})
        context = {
            # 侧边栏数据
            'all_silencers_count': all_silencers_count,
            'sources_silencers_count': sources_silencers_count,
            'species_silencers_count': species_silencers_count,
            'bio_sample_types_silencers_count': bio_sample_types_silencers_count,
            'tissue_types_select_data': tissue_types_select_data,
            'bio_sample_names_select_data': bio_sample_names_select_data,
        }
        return render(request, template_name=self.template_name, context=dict(self.context, **context))

    def post(self, request, *args, **kwargs):
        data: dict = request.json
        print(data)
        sources_chosen = data.get('sourcesChosen', [])
        species_chosen = data.get('speciesChosen', [])
        bio_sample_types_chosen = data.get('bioSampleTypesChosen', [])
        tissue_types_chosen = data.get('tissueTypesChosen', [])
        silencers = filtered_unknown_silencers()
        if sources_chosen:
            silencers = silencers.filter(sample__source__in=sources_chosen)
        if species_chosen:
            silencers = silencers.filter(sample__species__in=species_chosen)
        if bio_sample_types_chosen:
            silencers = silencers.filter(sample__bio_sample_type__in=bio_sample_types_chosen)
        if tissue_types_chosen:
            silencers = silencers.filter(sample__tissue_type__in=tissue_types_chosen)
        all_silencers_count = silencers.count()
        sources_chosen_silencers_count = silencers_classify_count('source', sources, silencers)
        species_chosen_silencers_count = silencers_classify_count('species', species, silencers)
        bio_sample_types_chosen_silencers_count = silencers_classify_count('bio_sample_type', bio_sample_types,
                                                                           silencers)
        tissue_types = list(
            Sample.objects.values_list('tissue_type', flat=True).distinct().exclude(tissue_type__in=['', 'unknown']))
        tissue_types_select_data = silencers_classify_count_filter_zero('tissue_type',
                                                                        {tissue_type: tissue_type for tissue_type in
                                                                         tissue_types}, silencers)
        bio_sample_names = list(Sample.objects.values_list('bio_sample_name', flat=True).distinct().exclude(
            bio_sample_name__in=['', 'unknown']))
        bio_sample_names_select_data = silencers_classify_count_filter_zero('bio_sample_name',
                                                                            {bio_sample_name: bio_sample_name for
                                                                             bio_sample_name in bio_sample_names},
                                                                            silencers)
        return JsonResponse({
            **self.context,
            'all_silencers_count': all_silencers_count,
            'sources_chosen_silencers_count': sources_chosen_silencers_count,
            'species_chosen_silencers_count': species_chosen_silencers_count,
            'bio_sample_types_chosen_silencers_count': bio_sample_types_chosen_silencers_count,
            'tissue_types_select_data': tissue_types_select_data,
            'bio_sample_names_select_data': bio_sample_names_select_data
        })
