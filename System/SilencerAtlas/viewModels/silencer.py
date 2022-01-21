# -*- encoding: utf-8 -*-
"""
@File Name      :   silencer.py    
@Create Time    :   2022/1/15 20:29
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

from django.db.models import Q

from SilencerAtlas.libs.lists import unknown_value_list, recognition_factors_value_list
from SilencerAtlas.models.silencer import Silencer


def filtered_unknown_silencers():
    return Silencer.objects.all().distinct().exclude(
        Q(sample__source__in=unknown_value_list) |
        Q(sample__species__in=unknown_value_list) |
        Q(sample__bio_sample_type__in=unknown_value_list) |
        Q(sample__tissue_type__in=unknown_value_list) |
        Q(sample__bio_sample_name__in=unknown_value_list)
    ).filter(recognition_factors__name__in=recognition_factors_value_list)


def filtered_sample_chosen_silencers(data):
    sources_chosen = data.get('sourcesChosen', [])
    species_chosen = data.get('speciesChosen', [])
    bio_sample_types_chosen = data.get('bioSampleTypesChosen', [])
    tissue_types_chosen = data.get('tissueTypesChosen', [])
    bio_sample_names_chosen = data.get('bioSamplesNamesChosen', [])
    silencers = filtered_unknown_silencers()
    if sources_chosen:
        silencers = silencers.filter(sample__source__in=sources_chosen)
    if species_chosen:
        silencers = silencers.filter(sample__species__in=species_chosen)
    if bio_sample_types_chosen:
        silencers = silencers.filter(sample__bio_sample_type__in=bio_sample_types_chosen)
    if tissue_types_chosen:
        silencers = silencers.filter(sample__tissue_type__in=tissue_types_chosen)
    if bio_sample_names_chosen:
        silencers = silencers.filter(sample__bio_sample_name__in=bio_sample_names_chosen)
    return silencers


def filter_zero_count(fields_count):
    return list(filter(lambda x: x.get('count', 0) != 0, fields_count))


def silencers_classify_count(search_field: str, field_values: dict, silencers=None):
    fields_count = []
    if not silencers:
        silencers = Silencer.objects.all()
    for field_key, field_value in field_values.items():
        filter_by = {'sample__' + search_field: field_key}
        filtered_silencers = silencers.filter(**filter_by)
        silencers_count = filtered_silencers.count()
        fields_count.append({'value': field_key, 'label': field_value, 'count': silencers_count})
    return fields_count


def silencers_classify_count_filter_zero(search_field: str, field_values: dict, silencers=None):
    return filter_zero_count(silencers_classify_count(search_field, field_values, silencers))
