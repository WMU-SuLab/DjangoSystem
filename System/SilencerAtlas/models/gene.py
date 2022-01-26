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

from .base import Base
from .region import Region


class Gene(Base):
    STRAND_ITEMS = [
        # 正链
        ('+', '+'),
        # 负链
        ('-', '-'),
        # 不需要指定
        ('.', '.'),
        # 不知道
        ('unknown', 'unknown')
    ]
    name = models.CharField(max_length=128,unique=True, db_index=True, verbose_name='基因名')
    ensembl_id = models.CharField(max_length=128,unique=True,db_index=True, null=True, blank=True, verbose_name='Ensembl数据库id')

    @property
    def gene_symbol(self):
        return self.name

    @gene_symbol.setter
    def gene_symbol(self, name):
        self.name = name

    region = models.OneToOneField(Region, verbose_name='基因区域',null=True,blank=True, db_index=True, on_delete=models.RESTRICT,
                                  related_name='gene')
    strand = models.CharField(max_length=10, null=True, blank=True, choices=STRAND_ITEMS, default='unknown',
                              verbose_name='正/负链信息')
    bio_type=models.CharField(max_length=128, null=True, blank=True,default='DNA', verbose_name='基因类型')


    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '基因'
        unique_together=(('name','ensembl_id','region','strand','bio_type'),)

    def __str__(self):
        return f'<Gene name: {self.name}>'


class GeneExpression(models.Model):
    """
    因为数据量太大，所以就不继承Base了，减少额外的信息
    """
    gene=models.ForeignKey(Gene, on_delete=models.CASCADE, related_name='gene_expressions', verbose_name='基因')
    bio_sample_name=models.CharField(max_length=128, null=False, blank=False,db_index=True, verbose_name='样本名')
    expression_value=models.JSONField(default=list,null=True,blank=True, verbose_name='表达情况')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '基因表达'
        unique_together=(('gene','bio_sample_name',),)

    def __str__(self):
        return f'<Gene expression: {self.gene}-{self.bio_sample_name}:{self.expression_value}>'