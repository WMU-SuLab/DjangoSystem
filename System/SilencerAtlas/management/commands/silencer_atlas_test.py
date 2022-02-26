# -*- encoding: utf-8 -*-
"""
@File Name      :   silencer_atlas_test.py.py    
@Create Time    :   2022/2/21 9:55
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
import os
from collections import defaultdict

import pandas as pd
from django.conf import settings
from django.db.models import Q

from SilencerAtlas.libs.model_choices import sources, species, bio_sample_types, recognition_factors, variants, \
    strategies
from SilencerAtlas.models.gene import Gene, GeneExpression
from SilencerAtlas.models.recognition_factor import RecognitionFactor
from SilencerAtlas.models.region import CommonRegion
from SilencerAtlas.models.sample import Sample
from SilencerAtlas.models.silencer import Silencer, SilencerRecognitionFactor, SilencerSampleRecognitionFactor, \
    SilencerSNP, SilencerTranscriptionFactor, SilencerGene, SilencerCas9
from SilencerAtlas.models.snp import SNP
from SilencerAtlas.viewModels.gene import to_genes_dict
from SilencerAtlas.viewModels.recognition_factor import to_recognition_factors_dict, recognition_factors_to_list
from SilencerAtlas.viewModels.region import divide_region, generate_region, to_regions_dict
from SilencerAtlas.viewModels.sample import to_samples_dict
from SilencerAtlas.viewModels.snp import to_snps_dict
from utils.file_handler.read import read_n_lines_each_time_yield
from utils.file_handler.table_handler.csv import read_csv_n_lines_each_time_by_pandas_yield
from utils.time import print_accurate_execute_time
from utils.command import BaseCommand
@print_accurate_execute_time
def init_test_database_data():
    """
    只适合完全为空或者只运行过test的数据库，否则会出错
    :return:
    """
    print('init test database data')
    count = 0
    for source_key in sources.keys():
        for species_key in species.keys():
            for bio_sample_type_key in bio_sample_types.keys():
                count += 1
                sample, sample_created = Sample.objects.get_or_create(
                    sample_id='test_sample' + str(count),
                    bio_sample_name='test_bio_sample_name' + str(count),
                    tissue_type='test_type' + str(count),
                    bio_sample_type=bio_sample_type_key,
                    species=species_key,
                    source=source_key
                )
                region, region_created = CommonRegion.objects.get_or_create(
                    chromosome='silencer_fake_chr' + str(count),
                    start=count * 10,
                    end=999999999
                )
                silencer, silencer_created = Silencer.objects.get_or_create(
                    silencer_id='test_silencer' + str(count),
                    region=region,
                    score=0, strand='+', sample=sample
                )
                for recognition_factor_key in recognition_factors.keys():
                    recognition_factor, recognition_factor_created = RecognitionFactor.objects.get_or_create(
                        name=recognition_factor_key
                    )
                    SilencerRecognitionFactor.objects.get_or_create(
                        silencer=silencer,
                        recognition_factor=recognition_factor,
                    )
                    SilencerSampleRecognitionFactor.objects.get_or_create(
                        silencer=silencer,
                        recognition_factor=recognition_factor,
                        bio_sample_name=sample.bio_sample_name,
                        z_score=1,
                        recognized=True
                    )
                snp, snp_created = SNP.objects.get_or_create(rs_id='test_snp' + str(count), region=region)
                for variant in variants.keys():
                    SilencerSNP.objects.get_or_create(silencer=silencer, snp=snp, variant=variant)
                gene, gene_created = Gene.objects.get_or_create(name='test_gene' + str(count), region=region)
                SilencerTranscriptionFactor.objects.get_or_create(silencer=silencer, transcription_factor=gene, binding_site=region)
                for strategy in strategies.keys():
                    SilencerGene.objects.get_or_create(silencer=silencer, gene=gene, strategy=strategy)
                SilencerCas9.objects.get_or_create(silencer=silencer, region=region)
    print('测试数据初始化完成，如果要删除测试数据建议直接重建数据库，速度更快')




@print_accurate_execute_time
def build_database_data():
    with open('D:\Coding\Python\Django-backend\System\SilencerAtlas\libs/silencers_all.txt', 'w') as w:
        w.write('\t'.join(
            ['silencer_id', 'chr', 'start', 'end', 'score', 'bio_sample_name', 'bio_sample_type', 'species', 'source',
             'recognition_factors']) + '\n')
        print('handle encode silencers')
        for rows in read_n_lines_each_time_yield('D:/Server/1.ENCODE.rSilencers.Browse', 100000, skip_rows=1):
            new_rows = []
            for row in rows:
                row = row.strip().split('\t')
                chromosome, start, end = divide_region(row[2])
                new_row = '\t'.join([row[0], chromosome, start, end, row[3], row[5], row[4], 'human', 'encode',
                                     recognition_factors_to_list(row[6])]) + '\n'
                new_rows.append(new_row)
            w.writelines(new_rows)
        print('handle roadmap silencers')
        for rows in read_n_lines_each_time_yield('D:/Server/1.Roadmap.rSilencers.Browse', 100000, skip_rows=1):
            new_rows = []
            for row in rows:
                row = row.strip().split('\t')
                chromosome, start, end = divide_region(row[2])
                new_row = '\t'.join([row[0], chromosome, start, end, row[3], row[5], row[4], 'human', 'roadmap',
                                     recognition_factors_to_list(row[6])]) + '\n'
                new_rows.append(new_row)
            w.writelines(new_rows)


class Command(BaseCommand):
    help = 'silencer atlas database command'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--test', action='store_true', help='init database for testing')
        parser.add_argument('-b', '--build', action='store_true', help='build silencers')
        super(Command, self).add_arguments(parser)


    def handle(self, *args, **options):
        test = options.get('test', False)
        build = options.get('build', False)
        if test:
            return init_test_database_data()
        elif build:
            return build_database_data()
