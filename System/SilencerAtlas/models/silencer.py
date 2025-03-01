# -*- encoding: utf-8 -*-
"""
@File Name      :   silencer.py    
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

from SilencerAtlas.libs.model_choices import unknown, strand, strategies, variants
from .base import Base
from .gene import Gene
from .recognition_factor import RecognitionFactor
from .region import CommonRegion
from .sample import Sample
from .snp import SNP


class Silencer(Base):
    STRAND_ITEMS = [(key, value) for key, value in strand.items() | unknown.items()]

    silencer_id = models.CharField(max_length=128, unique=True, db_index=True, verbose_name='沉默子id')
    # 沉默子名称，可以不需要
    silencer_name = models.CharField(max_length=128, null=True, blank=True, db_index=True, verbose_name='沉默子名称')
    # OneToOneField类似于 ForeignKey 与 unique=True
    # 一个区域对应多个silencer
    region = models.ForeignKey(CommonRegion, on_delete=models.CASCADE, null=True, blank=True, verbose_name='沉默子区域',
                               related_name='silencer')
    # score = models.FloatField(null=True, blank=True, default=0, verbose_name='评分')
    score = models.CharField(max_length=64, null=True, blank=True, default='', verbose_name='评分')

    @property
    def normalized_score(self):
        return self.score

    strand = models.CharField(max_length=10, null=True, blank=True, choices=STRAND_ITEMS, default='--',
                              verbose_name='正负链')

    # 关联了一对多、多对多的模型使用原模型的字段名作为属性名，而反向模型使用源模型名的小写形式，加上 '_set'，反向模型可以使用related_name自定义
    # 而调用多对多的中间模型只能通过源模型名的小写形式，加上 '_set'
    # related_query_name默认值就是related_name
    # relate_name是属性中用，related_query_name是filter或者其他查询方法中使用
    sample = models.ForeignKey(Sample, verbose_name='属于样本', db_index=True, null=True, blank=True,
                               on_delete=models.CASCADE, related_name='silencers')
    # dhs = models.ManyToManyField(DHSs, verbose_name='DHSs', db_index=True, through='SilencerDHS',
    #                              related_name='silencers')

    TFBs = models.ManyToManyField(Gene, verbose_name='转录因子结合位点', db_index=True, through='SilencerTranscriptionFactor',
                                  related_name='tf_silencers')
    SNPs = models.ManyToManyField(SNP, verbose_name='SNPs', db_index=True, through='SilencerSNP',
                                  related_name='silencers')
    recognition_factors = models.ManyToManyField(RecognitionFactor, verbose_name='识别因子情况', db_index=True,
                                                 through='SilencerRecognitionFactor',
                                                 related_name='recognized_silencers')
    # sample_recognition_factors_singles
    sample_recognition_factors_z_score = models.ManyToManyField(RecognitionFactor, verbose_name='识别因子在各个样本中的z-score',
                                                                db_index=True,
                                                                through='SilencerSampleRecognitionFactor',
                                                                related_name='z_scored_silencers')
    Cas9s = models.ManyToManyField(CommonRegion, verbose_name='Cas9s', db_index=True, through='SilencerCas9',
                                   related_name='silencers')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '沉默子'

    # 可以用于在admin页面的子模型的外键的选项中指定父模型
    def __str__(self):
        return f'<Silencer silencer_id:{self.silencer_id}>'


class SilencerGene(models.Model):
    STRATEGY_ITEMS = [(key, value) for key, value in strategies.items() | unknown.items()]
    silencer = models.ForeignKey(Silencer, on_delete=models.CASCADE, related_name='target_genes')
    gene_name = models.CharField(max_length=64, default='--', verbose_name='基因名称')
    gene_ensembl_id = models.CharField(max_length=128, default='--', verbose_name='基因ensembl_id')
    genomic_loci = models.CharField(max_length=128, default='--', verbose_name='基因位点')
    strategy = models.CharField(max_length=32, choices=STRATEGY_ITEMS, default='unknown', verbose_name='策略')
    sub_strategy = models.CharField(max_length=32, default='', verbose_name='子策略')
    distance_to_TSS = models.CharField(max_length=64, null=True, blank=True, default=0, verbose_name='距基因的TSS的距离')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '沉默子的靶基因'
        unique_together = (('silencer', 'gene_name', 'gene_ensembl_id', 'genomic_loci', 'strategy', 'sub_strategy'),)


class SilencerTranscriptionFactor(Base):
    silencer = models.ForeignKey(Silencer, on_delete=models.CASCADE)
    transcription_factor = models.ForeignKey(Gene, on_delete=models.CASCADE)
    binding_site = models.ForeignKey(CommonRegion,blank=True,null=True, on_delete=models.CASCADE,verbose_name='转录因子结合位点')

    experiment = models.CharField(max_length=255,null=True, blank=True, default=list,verbose_name='相关实验')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '沉默子的转录因子结合位点'
        unique_together = (('silencer', 'transcription_factor', 'binding_site'),)


class SilencerSNP(Base):
    VARIANTS_ITEMS = [(key, value) for key, value in variants.items() | unknown.items()]
    silencer = models.ForeignKey(Silencer, on_delete=models.CASCADE)
    snp = models.ForeignKey(SNP, on_delete=models.CASCADE)

    variant = models.CharField(max_length=32, choices=VARIANTS_ITEMS, default='--', verbose_name='策略')
    distance=models.IntegerField(null=True,blank=True,default=0,verbose_name='距离')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '沉默子的SNP'
        unique_together = (('silencer', 'snp', 'variant'),)


class SilencerRecognitionFactor(Base):
    silencer = models.ForeignKey(Silencer, on_delete=models.CASCADE)
    recognition_factor = models.ForeignKey(RecognitionFactor, on_delete=models.CASCADE)

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '沉默子在样本中被识别的修饰'
        unique_together = (('silencer', 'recognition_factor'),)


class SilencerSampleRecognitionFactor(models.Model):
    silencer = models.ForeignKey(Silencer, on_delete=models.CASCADE)
    recognition_factor = models.ForeignKey(RecognitionFactor, on_delete=models.CASCADE)
    # sample=models.ForeignKey(Sample, on_delete=models.CASCADE, verbose_name='样本')
    # express_level=models.FloatField(verbose_name='表达水平')
    # bio_sample_name = models.CharField(max_length=256, default='--', db_index=True, verbose_name='样本名称')
    # 占用空间太大了，而且用的比较少，决定删除索引
    bio_sample_name = models.CharField(max_length=256, default='--', verbose_name='样本名称')

    # 原来是每个样本一个表达水平的，现在把所有相同bio sample name的样本表达水平值合起来为z-score
    z_score = models.FloatField(null=True, blank=True, default=0, verbose_name='z-score')
    recognized = models.BooleanField(null=True, blank=True, default=False, verbose_name='是否识别')

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '沉默子在各个样本中修饰的z-score'
        unique_together = (('silencer', 'recognition_factor', 'bio_sample_name'),)


class SilencerCas9(Base):
    silencer = models.ForeignKey(Silencer, on_delete=models.CASCADE)
    region = models.ForeignKey(CommonRegion, on_delete=models.CASCADE)

    class Meta(Base.Meta):
        verbose_name = verbose_name_plural = '沉默子的CRISPR/Cas9'
        unique_together = (('silencer', 'region'),)
