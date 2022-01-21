# -*- encoding: utf-8 -*-
"""
@File Name      :   region.py    
@Create Time    :   2021/12/7 20:04
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


class Region(Base):
    """
    一个基因区域或者位点（左开右闭）
    """
    SPECIES_ITEMS = [
        ('human', 'Human'),
        ('mouse', 'Mouse'),
        ('other', 'Other'),
        ('unknown', 'unknown'),
    ]
    # 由于区域位置用的太多，所以必须重新设置为bigint
    id = models.BigAutoField(primary_key=True)
    chromosome = models.CharField(max_length=6, null=True, blank=True, db_index=True, default='chr1',
                                  verbose_name='染色体')

    # chr是Python内置变量
    @property
    def chr(self):
        return self.chromosome

    @chr.setter
    def chr(self, value):
        self.chromosome = value

    # 'max_length' is ignored when used with BigIntegerField.BigIntegerField 不需要max_length
    # 区域是左开右闭
    start = models.BigIntegerField(null=True, blank=True, db_index=True, default=0, verbose_name='起始位点')
    end = models.BigIntegerField(null=True, blank=True, db_index=True, default=1, verbose_name='终止位点')

    @property
    def length(self):
        return abs(self.end - self.start + 1)

    @property
    def size(self):
        return self.length

    @property
    def is_region(self):
        return self.length > 1

    @property
    def is_loci(self):
        return self.length == 1

    @property
    def is_locus(self):
        return self.is_loci

    @property
    def loci(self):
        return f'{self.chr}:{self.start}-{self.end}'

    @loci.setter
    def loci(self, value: str):
        chromosome, start_end = value.split(':')
        self.chromosome = chromosome
        start, end = start_end.split('-')
        self.start = int(start)
        self.end = int(end)

    @property
    def locus(self):
        return self.loci

    @property
    def location(self):
        return self.location

    species = models.CharField(max_length=64, choices=SPECIES_ITEMS, null=True, blank=True, db_index=True,
                               default='unknown', verbose_name='物种')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '基因组区域/位点'
        unique_together = (('chromosome', 'start', 'end'),)

    def __str__(self):
        return f'<Region/locus/loci:{self.loci}>'
