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

from SilencerAtlas.libs.lists import unknown_value_list
from SilencerAtlas.models.silencer import Silencer


def to_silencers_dict(silencers):
    return {silencer.silencer_id: silencer for silencer in silencers}


def filter_silencers_any(silencers, silencer_id):
    for silencer in silencers:
        if silencer.silencer_id == silencer_id:
            return silencer


def filtered_unknown_silencers():
    return Silencer.objects.exclude(
        Q(sample__source__in=unknown_value_list) |
        Q(sample__species__in=unknown_value_list) |
        Q(sample__bio_sample_type__in=unknown_value_list) |
        Q(sample__tissue_type__in=unknown_value_list) |
        Q(sample__bio_sample_name__in=unknown_value_list)
    )


def filtered_sample_chosen_silencers(data):
    sources_chosen = data.get('sourcesChosen', [])
    species_chosen = data.get('speciesChosen', [])
    bio_sample_types_chosen = data.get('bioSampleTypesChosen', [])
    tissue_types_chosen = data.get('tissueTypesChosen', [])
    bio_sample_names_chosen = data.get('bioSamplesNamesChosen', [])
    silencers = Silencer.objects.all()
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


def silencers_classify_count(search_field: str, field_values: dict, have_silencers=False, silencers=None):
    # 这样是因为用silencers判断会从数据库中读取silencers，非常慢
    if not have_silencers:
        silencers = Silencer.objects.all()
    return [{'value': field_key, 'label': field_value,
             'count': silencers.filter(**{'sample__' + search_field: field_key}).count()} for field_key, field_value in
            field_values.items()]


def silencers_classify_count_filter_zero(search_field: str, field_values: dict, have_silencers=False, silencers=None):
    return filter_zero_count(silencers_classify_count(search_field, field_values, have_silencers, silencers))
