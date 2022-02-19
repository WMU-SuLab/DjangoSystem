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
from SilencerAtlas.libs.model_choices import unknown,recognition_factors


class RecognitionFactor(Base):
    RECOGNITION_FACTOR_ITEMS = [(key,value) for key,value in recognition_factors.items()|unknown.items()]
    name = models.CharField(max_length=32, choices=RECOGNITION_FACTOR_ITEMS,unique=True, default='--', db_index=True,
                            verbose_name='识别因子名称')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '识别因子'

    def __str__(self):
        return '<Recognition factor: {}>'.format(self.name)
