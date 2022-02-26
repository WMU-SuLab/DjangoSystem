# -*- encoding: utf-8 -*-
"""
@File Name      :   silencer_atlas_update.py    
@Create Time    :   2022/2/14 14:33
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

from collections import defaultdict

from django.db.models import Q

from SilencerAtlas.models.recognition_factor import RecognitionFactor
from SilencerAtlas.models.region import CommonRegion
from SilencerAtlas.models.sample import Sample
from SilencerAtlas.models.silencer import Silencer, SilencerRecognitionFactor, SilencerSampleRecognitionFactor, \
    SilencerGene
from SilencerAtlas.viewModels.recognition_factor import to_recognition_factors_dict, recognition_factors_to_list
from SilencerAtlas.viewModels.region import to_regions_dict, generate_region
from SilencerAtlas.viewModels.sample import to_samples_dict
from utils.file_handler.table_handler.csv import read_csv_n_lines_each_time_by_pandas_yield
from utils.text_handler.lists import group_by_step
from utils.time import print_accurate_execute_time
from utils.command import BaseCommand


@print_accurate_execute_time
def update_silencers(file_path, chunk_size=10000, skip_rows=0):
    """
    100000/3min
    10-12hours
    """
    batch_size = int(chunk_size / 10)
    for df in read_csv_n_lines_each_time_by_pandas_yield(file_path, sep='\t', chunk_size=chunk_size,
                                                         skip_rows=skip_rows):
        chromosomes = df['chr'].drop_duplicates().str.lower().to_list()
        starts = df['start'].drop_duplicates().to_list()
        ends = df['end'].drop_duplicates().to_list()
        print('building regions')
        CommonRegion.objects.bulk_create([CommonRegion(
            chromosome=row['chr'].lower(),
            start=row['start'],
            end=row['end']
        ) for index, row in df.iterrows()], batch_size=batch_size, ignore_conflicts=True)
        regions = to_regions_dict(
            list(CommonRegion.objects.filter(chromosome__in=chromosomes).filter(Q(start__in=starts) | Q(end__in=ends))))
        bio_sample_names = df['bio_sample_name'].drop_duplicates().to_list()
        print('getting samples')
        samples = to_samples_dict(list(Sample.objects.filter(bio_sample_name__in=bio_sample_names)))
        print('building silencers')
        silencer_ids = df['silencer_id'].to_list()
        # 要主动加载到内存，否则很慢
        silencers = list(Silencer.objects.filter(silencer_id__in=silencer_ids))
        for index, row in df.iterrows():
            silencers[index % chunk_size].region = regions[
                generate_region(row['chr'].lower(), row['start'], row['end'])]
            silencers[index % chunk_size].score = row['score']
            silencers[index % chunk_size].sample = samples[row['bio_sample_name']]
        Silencer.objects.bulk_update(silencers, ['region', 'score', 'sample'], batch_size=batch_size)
        recognition_factors_all = to_recognition_factors_dict(list(RecognitionFactor.objects.all()))
        print('building silencer recognition factors')
        SilencerRecognitionFactor.objects.bulk_create([SilencerRecognitionFactor(
            silencer=silencers[index % chunk_size],
            recognition_factor=recognition_factors_all[recognition_factor.lower()]
        ) for index, row in df.iterrows()
            for recognition_factor in row['recognition_factors'].split(';') if recognition_factor],
            batch_size=batch_size,
            ignore_conflicts=True)


@print_accurate_execute_time
def update_samples_recognition_factors_z_score(file_path, chunk_size=100, skip_rows=0):
    """
    1000/min
    200hours
    reading 314001-315000 rows
    """
    batch_size = int(chunk_size * 10)
    for df in read_csv_n_lines_each_time_by_pandas_yield(file_path, sep='\t', chunk_size=chunk_size,
                                                         skip_rows=skip_rows):
        silencer_sample_recognition_factors_dict = {}
        bio_sample_names = set()
        for index, row in df.iterrows():
            sample = defaultdict(dict)
            for bio_sample_name_recognition_factors, score in row[1:].iteritems():
                bio_sample_name, recognition_factor = bio_sample_name_recognition_factors.split(':')
                recognition_factor = recognition_factor.lower()
                bio_sample_names.add(bio_sample_name)
                sample[bio_sample_name][recognition_factor] = score
            silencer_sample_recognition_factors_dict[row['SilencerID']] = sample
        bio_sample_names = list(bio_sample_names)
        silencer_ids = df['SilencerID'].to_list()
        silencers = list(Silencer.objects.filter(silencer_id__in=silencer_ids))
        recognition_factors_all = to_recognition_factors_dict(list(RecognitionFactor.objects.all()))
        print('building silencer sample recognition factors')
        SilencerSampleRecognitionFactor.objects.bulk_create([SilencerSampleRecognitionFactor(
            silencer=silencers[index % chunk_size],
            bio_sample_name=bio_sample_name,
            recognition_factor=recognition_factors_all[recognition_factor],
        ) for index, silencers_item in enumerate(silencer_sample_recognition_factors_dict.items())
            for bio_sample_name, recognition_factors in silencers_item[1].items()
            for recognition_factor, score in recognition_factors.items()], batch_size=batch_size, ignore_conflicts=True)
        silencer_sample_recognition_factors = list(SilencerSampleRecognitionFactor.objects.filter(
            silencer__in=silencers,
            bio_sample_name__in=bio_sample_names
        ).prefetch_related('silencer', 'recognition_factor'))
        print('updating silencer sample recognition factors')
        for item in silencer_sample_recognition_factors:
            silencer_sample = silencer_sample_recognition_factors_dict[item.silencer.silencer_id][item.bio_sample_name]
            if item.recognition_factor.name in silencer_sample:
                item.z_score = silencer_sample[item.recognition_factor.name]
        SilencerSampleRecognitionFactor.objects.bulk_update(silencer_sample_recognition_factors, fields=['z_score'],
                                                            batch_size=batch_size)


@print_accurate_execute_time
def update_samples_recognition_factors_recognized(file_path, chunk_size=100, skip_rows=0):
    """
    1000/15s
    10000/2.5min
    50hours
    """

    batch_size = int(chunk_size * 10)
    for df in read_csv_n_lines_each_time_by_pandas_yield(file_path, sep='\t', chunk_size=chunk_size,
                                                         skip_rows=skip_rows):
        silencer_sample_recognition_factors_dict = {
            row['SilencerID']: {
                bio_sample_name: [
                    recognition_factor.lower() for recognition_factor in
                    recognition_factors_to_list(recognition_factors).split(';') if recognition_factor]
                for bio_sample_name, recognition_factors in row[1:].iteritems()
            } for index, row in df.iterrows()}
        silencer_ids = df['SilencerID'].to_list()
        silencers = list(Silencer.objects.filter(silencer_id__in=silencer_ids))
        bio_sample_names = df.columns.tolist()[1:]
        recognition_factors_all = to_recognition_factors_dict(list(RecognitionFactor.objects.all()))
        print('building silencer sample recognition factors')
        SilencerSampleRecognitionFactor.objects.bulk_create([SilencerSampleRecognitionFactor(
            silencer=silencers[index % chunk_size],
            bio_sample_name=bio_sample_name,
            recognition_factor=recognition_factors_all[recognition_factor.lower()],
        ) for index, silencers_item in enumerate(silencer_sample_recognition_factors_dict.items())
            for bio_sample_name, recognition_factors in silencers_item[1].items()
            for recognition_factor in recognition_factors], batch_size=batch_size, ignore_conflicts=True)
        silencer_sample_recognition_factors = list(SilencerSampleRecognitionFactor.objects.filter(
            silencer__in=silencers,
            bio_sample_name__in=bio_sample_names,
        ).prefetch_related('silencer', 'recognition_factor'))
        print('updating silencer sample recognition factors')
        for item in silencer_sample_recognition_factors:
            if item.recognition_factor.name in silencer_sample_recognition_factors_dict[item.silencer.silencer_id][
                item.bio_sample_name]:
                item.recognized = True
        SilencerSampleRecognitionFactor.objects.bulk_update(silencer_sample_recognition_factors, fields=['recognized'],
                                                            batch_size=batch_size)


@print_accurate_execute_time
def update_target_genes(file_path, chunk_size=10000, skip_rows=0):
    """
    100000/1.5min
    3hours
    """
    batch_size = int(chunk_size / 10)
    for df in read_csv_n_lines_each_time_by_pandas_yield(file_path, sep='\t', chunk_size=chunk_size,
                                                         skip_rows=skip_rows):
        silencer_ids = df['silencerID'].to_list()
        silencers = list(Silencer.objects.filter(silencer_id__in=silencer_ids))
        silencer_target_genes_dict = {}
        # gene_names = []
        for index, row in df.iterrows():
            strategies = {}
            for group in group_by_step(list(row[1:].iteritems()), step=4):
                strategy = group[0][0].split('.')[0]
                if group[0][1] != '--':
                    if strategy == 'overlap':
                        strategies['spacial_overlap'] = {'gene_name': group[2][1], 'gene_ensembl_id': group[1][1],
                                                         'genomic_loci': group[0][1], 'distance': group[3][1],
                                                         'sub_strategy': group[0][0].split('.')[1]}
                    elif strategy == 'nearest':
                        strategies['physical_nearest'] = {'gene_name': group[2][1], 'gene_ensembl_id': group[1][1],
                                                          'genomic_loci': group[0][1], 'distance': group[3][1], }
                    elif strategy == 'homer':
                        strategies['homer_nearest'] = {'gene_name': group[2][1], 'gene_ensembl_id': group[1][1],
                                                       'genomic_loci': group[0][1], 'distance': group[3][1], }
                    # gene_names.append(group[2][1])
            silencer_target_genes_dict[row['silencerID']] = strategies
        SilencerGene.objects.bulk_create([SilencerGene(
            silencer=silencers[index % chunk_size],
            gene_name=value['gene_name'],
            gene_ensembl_id=value['gene_ensembl_id'],
            genomic_loci=value['genomic_loci'],
            strategy=strategy,
            sub_strategy=value.get('sub_strategy', ''),
            distance_to_TSS=value['distance'],
        ) for index, silencers_item in enumerate(silencer_target_genes_dict.items())
            for strategy, value in silencers_item[1].items()], batch_size=batch_size, ignore_conflicts=True)
        # Gene.objects.bulk_create([Gene(name=name) for name in gene_names], batch_size=batch_size, ignore_conflicts=True)


class Command(BaseCommand):
    help = 'silencer atlas database update subdivide command'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--silencer', action='store_true', help='update silencers')
        parser.add_argument('-t', '--target_gene', action='store_true', help='update silencers target genes')
        parser.add_argument('-z', '--z_score', action='store_true',
                            help='update silencers samples recognition factors score')
        parser.add_argument('-r', '--recognized', action='store_true',
                            help='update silencers samples recognition factors recognized')
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        chunk_size = options.get('chunk_size', 1000)
        skip_rows = options.get('skip_rows', 0)
        file_path = options.get('file_path', None)
        if file_path is None:
            print('Please input file path')
            return
        update_silencer = options.get('silencer', None)
        update_target_gene = options.get('target_gene', None)
        update_z_score = options.get('z_score', None)
        update_recognized = options.get('recognized', None)
        kargs={}
        if chunk_size:
            kargs['chunk_size'] = chunk_size
        if skip_rows:
            kargs['skip_rows'] = skip_rows
        if [update_silencer, update_target_gene, update_z_score, update_recognized].count(True) == 0:
            print('Please input update type')
            return
        elif [update_silencer, update_target_gene, update_z_score, update_recognized].count(True) > 1:
            print('Please input only one update type')
            return
        elif update_silencer:
            return update_silencers(file_path, **kargs)
        elif update_target_gene:
            return update_target_genes(file_path, **kargs)
        elif update_z_score:
            return update_samples_recognition_factors_z_score(file_path, **kargs)
        elif update_recognized:
            return update_samples_recognition_factors_recognized(file_path, **kargs)
