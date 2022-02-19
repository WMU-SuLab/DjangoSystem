# -*- encoding: utf-8 -*-
"""
@File Name      :   dhs.py    
@Create Time    :   2021/12/7 20:11
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
from .region import Region


# DNase I hyper sensitivity sites
class DHS(Base):
    dhs_id = models.CharField(max_length=128, default='--', verbose_name='DHS id')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='区域')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = 'DHS'

    def __str__(self):
        return '<DHS id: >'.format(self.dhs_id)
