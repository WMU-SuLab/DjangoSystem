# -*- encoding: utf-8 -*-
"""
@File Name      :   sample.py    
@Create Time    :   2021/12/7 19:56
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

from django.db import models

from SilencerAtlas.libs.model_choices import unknown, bio_sample_types, species, sources
from .base import Base


class Sample(Base):
    BIO_SAMPLE_TYPE_ITEMS = [(key, value) for key, value in bio_sample_types.items() | unknown.items()]
    SPECIES_ITEMS = [(key, value) for key, value in species.items() | unknown.items()]
    SOURCE_ITEMS = [(key, value) for key, value in sources.items() | unknown.items()]

    # 目前由于直接整合了数据，没有多个样本了，一个sample_name只有一个样本，所以不需要sample_id,只需要sample_name就可以了
    # 但是为了扩充后期可能的需求，此字段还是保留
    sample_id = models.CharField(max_length=128, null=True, blank=True, db_index=True, verbose_name='样本的id')

    bio_sample_name = models.CharField(max_length=256, default='--', db_index=True, unique=True,
                                       verbose_name='样本名称')
    tissue_type = models.CharField(max_length=128, default='--', unique=True, blank=True, db_index=True,
                                   verbose_name='组织或细胞类型')

    @property
    def tissue_cell_type(self):
        return self.tissue_type

    @tissue_cell_type.setter
    def tissue_cell_type(self, value):
        self.tissue_type = value

    bio_sample_type = models.CharField(max_length=128, choices=BIO_SAMPLE_TYPE_ITEMS, default='--',
                                       verbose_name='样本类型')
    species = models.CharField(max_length=64, choices=SPECIES_ITEMS, default='--', verbose_name='物种')
    source = models.CharField(max_length=32, choices=SOURCE_ITEMS, default='--', verbose_name='来源数据库')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '样本'

    def __str__(self):
        return f'<Sample id:{self.sample_id}>'
