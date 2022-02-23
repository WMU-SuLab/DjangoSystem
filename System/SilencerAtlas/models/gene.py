# -*- encoding: utf-8 -*-
"""
@File Name      :   gene.py    
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

from SilencerAtlas.libs.model_choices import unknown, strand
from .base import Base
from .region import CommonRegion


class Gene(Base):
    STRAND_ITEMS = [(key, value) for key, value in strand.items() | unknown.items()]
    # 默认的'--'就是 unknown 的意思
    name = models.CharField(max_length=128, db_index=True, default='--', verbose_name='基因名')
    ensembl_id = models.CharField(max_length=128, unique=True, db_index=True, null=True, blank=True, default='--',
                                  verbose_name='Ensembl数据库id')

    @property
    def gene_symbol(self):
        return self.name

    @gene_symbol.setter
    def gene_symbol(self, name):
        self.name = name

    strand = models.CharField(max_length=10, null=True, blank=True, choices=STRAND_ITEMS, default='.',
                              verbose_name='正/负链信息')
    bio_type = models.CharField(max_length=128, null=True, blank=True, default='DNA', verbose_name='基因类型')
    regions = models.ManyToManyField(CommonRegion, verbose_name='基因区域', db_index=True, through='GeneRegion',
                                     related_name='genes')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '基因'
        unique_together = (('name', 'ensembl_id', 'strand', 'bio_type'),)

    def __str__(self):
        return f'<Gene name: {self.name}>'


class GeneRegion(Base):
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE, verbose_name='基因')
    region = models.ForeignKey(CommonRegion, on_delete=models.CASCADE, verbose_name='区域')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '基因区域'
        unique_together = (('gene', 'region'),)

    def __str__(self):
        return f'<Gene region: {self.gene}&{self.region}>'


class GeneExpression(models.Model):
    """
    因为数据量太大，所以就不继承Base了，减少额外的信息
    """
    gene_name = models.CharField(max_length=128, null=False,blank=False,db_index=True, verbose_name='基因名')
    bio_sample_name = models.CharField(max_length=128, null=False, blank=False, db_index=True, verbose_name='样本名')
    expression_value = models.JSONField(default=list, null=True, blank=True, verbose_name='表达情况')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '基因表达'
        unique_together = (('gene_name', 'bio_sample_name',),)

    def __str__(self):
        return f'<Gene expression: {self.gene_name}-{self.bio_sample_name}:{self.expression_value}>'
