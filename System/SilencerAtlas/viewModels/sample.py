# -*- encoding: utf-8 -*-
"""
@File Name      :   sample.py    
@Create Time    :   2022/1/8 17:06
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

from SilencerAtlas.models.silencer import Silencer

def filter_samples_any(samples,bio_sample_name):
    for sample in samples:
        if sample.bio_sample_name==bio_sample_name:
            return sample

# def bio_samples_classify_count(search_field, field_list):
#     # filter_by = {search_field + '__in': lower_underline_list(field_list)}
#     filter_by = {search_field + '__in': field_list}
#     field_chosen_bio_sample_names = list(Sample.objects.filter(**filter_by).values_list(
#         'bio_sample_name', flat=True).distinct().exclude(bio_sample_name='unknown'))
#     field_chosen_bio_sample_names_count = len(field_chosen_bio_sample_names)
#     return field_chosen_bio_sample_names, field_chosen_bio_sample_names_count
