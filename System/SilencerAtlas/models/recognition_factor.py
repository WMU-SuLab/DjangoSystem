# -*- encoding: utf-8 -*-
"""
@File Name      :   recognition_factor.py    
@Create Time    :   2021/12/7 20:03
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

from .base import Base


class RecognitionFactor(Base):
    RECOGNITION_FACTOR_ITEMS = [
        ('h3k27me3', 'H3K27me3'),
        ('h3k9me1', 'H3K9me1'),
        ('h3k9me2', 'H3K9me2'),
        ('h3k9me3', 'H3K9me3'),
        ('h4k20me1', 'H4K20me1'),
        ('h3k79me3', 'H3K79me3'),
        ('unknown', 'unknown'),
    ]
    name = models.CharField(max_length=32, choices=RECOGNITION_FACTOR_ITEMS,unique=True, default='unknown', db_index=True,
                            verbose_name='识别因子名称')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '识别因子'

    def __str__(self):
        return '<Recognition factor: {}>'.format(self.name)
