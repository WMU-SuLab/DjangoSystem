# -*- encoding: utf-8 -*-
"""
@File Name      :   snp.py    
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
from .region import CommonRegion


# Single Nucleotide Polymorphism
class SNP(Base):
    rs_id = models.CharField(max_length=128, db_index=True, verbose_name='reference SNP id')

    @property
    def snp_id(self):
        return self.rs_id

    @snp_id.setter
    def snp_id(self, value):
        self.rs_id = value

    region = models.OneToOneField(CommonRegion, blank=True, null=True, on_delete=models.CASCADE, verbose_name='SNP位置',
                                  related_name='snp')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '单核苷酸多态性'

    def __str__(self):
        return f'<rs_id:{self.rs_id}>'
