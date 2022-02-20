# -*- encoding: utf-8 -*-
"""
@File Name      :   silencer_atlas_data.py    
@Create Time    :   2021/12/31 13:52
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

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from SilencerAtlas.libs.model_choices import sources, species, bio_sample_types, recognition_factors, variants, \
    strategies
from SilencerAtlas.models.gene import Gene, GeneExpression
from SilencerAtlas.models.recognition_factor import RecognitionFactor
from SilencerAtlas.models.region import Region
from SilencerAtlas.models.sample import Sample
from SilencerAtlas.models.silencer import Silencer, SilencerRecognitionFactors, SilencerSampleRecognitionFactors, \
    SilencerSNPs, SilencerTFBs, \
    SilencerGenes, SilencerCas9s
from SilencerAtlas.models.snp import SNP
from SilencerAtlas.viewModels.gene import to_genes_dict
from SilencerAtlas.viewModels.recognition_factor import to_recognition_factors_dict, recognition_factors_to_list
from SilencerAtlas.viewModels.region import divide_region, generate_region, to_regions_dict
from SilencerAtlas.viewModels.sample import to_samples_dict
from SilencerAtlas.viewModels.snp import to_snps_dict
from utils.file_handler.read import read_n_lines_each_time_yield
from utils.file_handler.table_handler.csv import read_csv_n_lines_each_time_by_pandas_yield
from utils.time import print_accurate_execute_time


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
                region, region_created = Region.objects.get_or_create(
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
                    SilencerRecognitionFactors.objects.get_or_create(
                        silencer=silencer,
                        recognition_factor=recognition_factor,
                    )
                    SilencerSampleRecognitionFactors.objects.get_or_create(
                        silencer=silencer,
                        recognition_factor=recognition_factor,
                        bio_sample_name=sample.bio_sample_name,
                        z_score=1,
                        recognized=True
                    )
                snp, snp_created = SNP.objects.get_or_create(rs_id='test_snp' + str(count), region=region)
                for variant in variants.keys():
                    SilencerSNPs.objects.get_or_create(silencer=silencer, snp=snp, variant=variant)
                gene, gene_created = Gene.objects.get_or_create(name='test_gene' + str(count), region=region)
                SilencerTFBs.objects.get_or_create(silencer=silencer, transcription_factor=gene, binding_site=region)
                for strategy in strategies.keys():
                    SilencerGenes.objects.get_or_create(silencer=silencer, gene=gene, strategy=strategy)
                SilencerCas9s.objects.get_or_create(silencer=silencer, region=region)
    print('测试数据初始化完成，如果要删除测试数据建议直接重建数据库，速度更快')


@print_accurate_execute_time
def init_database_data(dir_path):
    """
    初始化数据：包括识别因子数据，基因数据，snp数据，Cas9
    :param dir_path:
    :return:
    """
    # 先初始化识别因子的数据
    chunk_size = 10000
    batch_size = 1000
    if not dir_path:
        dir_path = os.path.join(settings.BASE_DIR, 'SilencerAtlas/libs')
    print('import recognition factors data')
    RecognitionFactor.objects.bulk_create([RecognitionFactor(
        name=name
    ) for name in recognition_factors.keys()], batch_size=batch_size, ignore_conflicts=True)
    # 初始化基因数据
    print('import gene data')
    genes_df = pd.read_csv(os.path.join(dir_path, 'genes.bed'),
                           sep='\t', names=['chr', 'start', 'end', 'strand', 'ensembl_id', 'gene_symbol', 'bio_type'])
    regions_df = genes_df[['chr', 'start', 'end', ]]
    chromosomes = list(set(['chr' + row['chr'] for index, row in regions_df.iterrows()]))
    starts = regions_df['start'].to_list()
    ends = regions_df['end'].to_list()
    Region.objects.bulk_create([Region(
        chromosome='chr' + row['chr'],
        start=row['start'],
        end=row['end'],
    ) for index, row in regions_df.iterrows()], batch_size=batch_size,
        ignore_conflicts=True)
    regions = to_regions_dict(
        list(Region.objects.filter(chromosome__in=chromosomes).filter(Q(start__in=starts) | Q(end__in=ends))))
    Gene.objects.bulk_create([Gene(
        name=row['gene_symbol'],
        ensembl_id=row['ensembl_id'],
        region=regions[generate_region(chromosome='chr' + row['chr'], start=row['start'], end=row['end'])],
        strand=row['strand'],
        bio_type=row['bio_type']
    ) for index, row in genes_df.iterrows()], batch_size=batch_size, ignore_conflicts=True)
    # 初始化基因样本数据
    print('import gene expressions data')
    # 样本名称对应表
    samples_ensembl_id_df = pd.read_csv(
        os.path.join(dir_path, 'sample_map.txt'),
        sep='\t', )
    samples_name = {row['SAMPID']: row['SMTSD'] for index, row in samples_ensembl_id_df.iterrows()}
    # 基因在各个样本中的表达数据
    # 这个文件比较大，必须分开读取；因为文件前两行没有用所以跳过，大约5万多行
    for gene_sample_expressions_df in read_csv_n_lines_each_time_by_pandas_yield(
            os.path.join(dir_path, 'gene_expressions.gct'), sep='\t',
            chunk_size=chunk_size, skip_rows=2):
        gene_names = gene_sample_expressions_df['Description'].tolist()
        print('bulk create gene')
        Gene.objects.bulk_create([Gene(name=name) for name in gene_names], batch_size=batch_size, ignore_conflicts=True)
        genes = to_genes_dict(list(Gene.objects.filter(name__in=gene_names)))
        gene_samples = {}
        for index, row in gene_sample_expressions_df.iterrows():
            sample_expression = {}
            for col_name, value in row[2:].iteritems():
                if sample_expression.get(samples_name[col_name], None):
                    sample_expression[samples_name[col_name]].append(value)
                else:
                    sample_expression[samples_name[col_name]] = [value]
            gene_samples[row['Description']] = sample_expression
        print('bulk create gene expressions')
        GeneExpression.objects.bulk_create(
            [GeneExpression(
                gene=genes[gene_name],
                bio_sample_name=bio_sample_name,
                expression_value=value,
            ) for gene_name, sample_expression in gene_samples.items() for bio_sample_name, value in
                sample_expression.items()],
            batch_size=batch_size,
            ignore_conflicts=True
        )
    # 初始化snp数据

    # 初始化Cas9数据

    print('初始化数据完成')


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


@print_accurate_execute_time
def pre_update_database_data(file_path):
    chunk_size = 10000
    batch_size = chunk_size
    for df in read_csv_n_lines_each_time_by_pandas_yield(file_path, sep='\t', chunk_size=chunk_size):
        silencer_ids = df['silencer_id'].to_list()
        print('building silencers')
        Silencer.objects.bulk_create([Silencer(
            silencer_id=silencer_id,
        ) for silencer_id in silencer_ids], batch_size=batch_size, ignore_conflicts=True)
        columns = df.columns.to_list()
        if 'bio_sample_name' not in columns:
            print('no bio_sample_name')
            return
        sample_column = list(
            {'sample_id', 'bio_sample_name', 'tissue_cell_type', 'bio_sample_type', 'species', 'source'} & set(columns))
        bio_sample_names = df['bio_sample_name'].drop_duplicates().to_list()
        samples_df = df[sample_column].drop_duplicates()
        print('building samples')
        Sample.objects.bulk_create([Sample(
            bio_sample_name=bio_sample_name,
        ) for bio_sample_name in bio_sample_names], batch_size=batch_size, ignore_conflicts=True)
        samples = to_samples_dict(list(Sample.objects.filter(bio_sample_name__in=bio_sample_names)))
        new_samples = []
        for index, row in samples_df.iterrows():
            sample = samples[row['bio_sample_name']]
            sample.sample_id = row.get('sample_id', '')
            sample.tissue_type = row.get('tissue_cell_type', row['bio_sample_name'])
            sample.bio_sample_type = row['bio_sample_type'].lower()
            sample.species = row.get('species', 'human').lower()
            sample.source = row.get('source', 'encode').lower()
            new_samples.append(sample)
        Sample.objects.bulk_update(new_samples,
                                   fields=['sample_id', 'tissue_type', 'bio_sample_type', 'species', 'source'],
                                   batch_size=batch_size)


@print_accurate_execute_time
def update_database_data(file_path):
    chunk_size = 10000
    batch_size = chunk_size / 10
    for df in read_csv_n_lines_each_time_by_pandas_yield(file_path, sep='\t', chunk_size=chunk_size):
        # 构建区域数据
        print('building regions')
        chromosomes = [item.lower() for item in df['chr'].drop_duplicates().to_list()]
        starts = df['start'].to_list()
        ends = df['end'].to_list()
        Region.objects.bulk_create([Region(
            chromosome=row['chr'].lower(),
            start=row['start'],
            end=row['end'],
        ) for index, row in df.iterrows()], batch_size=batch_size, ignore_conflicts=True)
        regions = to_regions_dict(
            list(Region.objects.filter(chromosome__in=chromosomes).filter(Q(start__in=starts) | Q(end__in=ends))))
        bio_sample_names = df['bio_sample_name'].drop_duplicates().to_list()
        samples = to_samples_dict(list(Sample.objects.filter(bio_sample_name__in=bio_sample_names)))
        print('building silencers')
        silencer_ids = df['silencer_id'].to_list()
        silencers = list(Silencer.objects.filter(silencer_id__in=silencer_ids))
        # 构建silencer基础数据
        for index, row in df.iterrows():
            silencers[index % chunk_size].silencer_name = row.get('silencer_name', '')
            silencers[index % chunk_size].strand = row.get('strand', '.')
            silencers[index % chunk_size].region = regions[
                generate_region(row['chr'].lower(), row['start'], row['end'])]
            silencers[index % chunk_size].score = row.get('score', 0)
            silencers[index % chunk_size].sample = samples[row['bio_sample_name']]
        Silencer.objects.bulk_update(silencers, ['silencer_name', 'strand', 'region', 'score', 'sample'],
                                     batch_size=batch_size)
        print('deleting silencers related data')
        SilencerGenes.objects.filter(silencer__in=silencers).delete()
        SilencerTFBs.objects.filter(silencer__in=silencers).delete()
        SilencerSNPs.objects.filter(silencer__in=silencers).delete()
        SilencerRecognitionFactors.objects.filter(silencer__in=silencers).delete()
        SilencerSampleRecognitionFactors.objects.filter(silencer__in=silencers).delete()
        SilencerCas9s.objects.filter(silencer__in=silencers).delete()
        # 构建靶基因数据
        # todo:靶基因构建方式需要更改
        if 'target_genes' in df.columns:
            print('building target genes')
            silencer_genes = df['target_genes']
            gene_names = list(set([gene_symbol for index, value in silencer_genes.items() for gene_symbol, strategy in
                                   map(lambda item: item.split(':'), value.split(';'))]))
            Gene.objects.bulk_create([Gene(name=name) for name in gene_names], batch_size=batch_size,
                                     ignore_conflicts=True)
            genes = to_genes_dict(list(Gene.objects.filter(name__in=gene_names)))
            SilencerGenes.objects.bulk_create([SilencerGenes(
                silencer=silencers[index % chunk_size],
                gene_name=genes[gene_symbol],
                strategy=strategy.lower()
            ) for index, value in silencer_genes.items()
                for gene_symbol, strategy in map(lambda item: item.split(':'), value.split(';')) if gene_symbol],
                batch_size=1000)
        # 构建TFBs数据
        if 'TFBs' in df.columns:
            print('building TFBs')
            silencer_tfbs = df['TFBs']
            gene_names = list(set([gene_symbol for index, value in silencer_tfbs.items() for gene_symbol in
                                   map(lambda item: item.split('~')[0], value.split(';'))]))
            Gene.objects.bulk_create([Gene(name=name) for name in gene_names], batch_size=batch_size,
                                     ignore_conflicts=True)
            genes = to_genes_dict(list(Gene.objects.filter(name__in=gene_names)))
            locations = []
            chromosomes = []
            starts = []
            ends = []
            for index, value in silencer_tfbs.items():
                for gene_symbol, binding_site in map(
                        lambda item: (item.split('~')[0], divide_region(item.split('~')[1])), value.split(';')):
                    chromosomes.append(binding_site[0])
                    starts.append(binding_site[1])
                    ends.append(binding_site[2])
                    locations.append(binding_site)
            chromosomes = list(set(chromosomes))
            Region.objects.bulk_create(
                [Region(chromosome=chromosome, start=start, end=end) for chromosome, start, end in locations],
                batch_size=batch_size, ignore_conflicts=True)
            regions = to_regions_dict(
                list(Region.objects.filter(chromosome__in=chromosomes).filter(Q(start__in=starts) | Q(end__in=ends))))
            SilencerTFBs.objects.bulk_create([SilencerTFBs(
                silencer=silencers[index % chunk_size],
                transcription_factor=genes[gene_symbol],
                binding_site=regions[generate_region(binding_site[0], binding_site[1], binding_site[2])],
            ) for index, value in silencer_tfbs.items()
                for gene_symbol, binding_site in
                map(lambda item: (item.split('~')[0], divide_region(item.split('~')[1])), value.split(';'))],
                batch_size=batch_size, )
        # 构建SNPs数据
        if 'SNPs' in df.columns:
            print('building SNPs')
            silencer_snps = df['SNPs']
            rs_ids = list(set([rs_id for index, value in silencer_snps.items()
                               for rs_id, variant in map(lambda item: item.split(':'), value.split(';'))]))
            SNP.objects.bulk_create([SNP(rs_id=rs_id) for rs_id in rs_ids], batch_size=batch_size,
                                    ignore_conflicts=True)
            snps = to_snps_dict(list(SNP.objects.filter(rs_id__in=rs_ids)))
            SilencerSNPs.objects.bulk_create([SilencerSNPs(
                silencer=silencers[index % chunk_size],
                snp=snps[rs_id],
                variant=variant.lower(),
            ) for index, value in silencer_snps.items()
                for rs_id, variant in map(lambda item: item.split(':'), value.split(';'))], batch_size=batch_size,
                ignore_conflicts=True)
        # 构建Recognition Factors数据
        if 'recognition_factors' in df.columns:
            print('building recognition factors')
            silencer_recognition_factors = df['recognition_factors']
            recognition_factors_all = to_recognition_factors_dict(list(RecognitionFactor.objects.all()))
            SilencerRecognitionFactors.objects.bulk_create([SilencerRecognitionFactors(
                silencer=silencers[index % chunk_size],
                recognition_factor=recognition_factors_all[recognition_factor.lower()],
            ) for index, value in silencer_recognition_factors.items() for recognition_factor in value.split(';')],
                batch_size=batch_size, ignore_conflicts=True)
        if 'samples_recognition_factors_z_score' in df.columns:
            print('building sample recognition factors z_score')
            silencer_sample_recognition_factors = df['samples_recognition_factors_z_score']
            recognition_factors_all = to_recognition_factors_dict(list(RecognitionFactor.objects.all()))
            SilencerSampleRecognitionFactors.objects.bulk_create([SilencerSampleRecognitionFactors(
                silencer=silencers[index % chunk_size],
                recognition_factor=recognition_factors_all[recognition_factor.lower()],
                bio_sample_name=bio_sample_name,
                z_score=float(z_score),
                recognized=bool(recognized),
            ) for index, value in silencer_sample_recognition_factors.items() for
                bio_sample_name, recognition_factor, recognized, z_score in
                map(lambda item: (*item.split(':')[0].split('-'), item.split(':')[1]), value.split(';'))],
                batch_size=batch_size, )
        # 构建Cas9s数据
        if 'Cas9s' in df.columns:
            print('building Cas9s')
            silencer_cas9s = df['Cas9s']
            locations = []
            chromosomes = []
            starts = []
            ends = []
            for index, value in silencer_cas9s.items():
                for chromosome, start, end in map(lambda item: divide_region(item), value.split(';')):
                    chromosomes.append(chromosome)
                    starts.append(start)
                    ends.append(end)
                    locations.append((chromosome, start, end))
            chromosomes = list(set(chromosomes))
            Region.objects.bulk_create(
                [Region(chromosome=chromosome, start=start, end=end) for chromosome, start, end in locations],
                batch_size=batch_size, ignore_conflicts=True)
            regions = to_regions_dict(
                list(Region.objects.filter(chromosome__in=chromosomes).filter(Q(start__in=starts) | Q(end__in=ends))))
            SilencerCas9s.objects.bulk_create([SilencerCas9s(
                silencer=silencers[index % chunk_size],
                region=regions[generate_region(chromosome, start, end)],
            ) for index, value in silencer_cas9s.items() for chromosome, start, end in
                map(lambda item: divide_region(item), value.split(';'))], batch_size=batch_size, )
    print('更新数据完成')


@print_accurate_execute_time
def delete_database_data(file_path, include=True):
    """
    删除silencer相关的数据，其他数据因为用不到不展示所以可以不用删，占空间一般也不大
    :param file_path: 文件路径
    :param include: 是按包含这些silencer还是排除这些silencer进行删除
    :return:
    """
    # 删除的数据一般都不大，所以直接全部读进来
    silencer_ids = pd.read_csv(file_path, sep='\t')['silencer_id'].to_list()
    # 因为设置了级联，所以直接删除silencer即可
    if include:
        Silencer.objects.filter(silencer_id__in=silencer_ids).delete()
    else:
        Silencer.objects.exclude(silencer_id__in=silencer_ids).delete()
    print('删除数据完成')


def delete_database_data_all():
    Silencer.objects.all().delete()
    print('删除全部主要数据完成')


@print_accurate_execute_time
def export_database_data(file_path):
    silencers = Silencer.objects.prefetch_related(
        'region',
        'sample',
        'silencergenes_set',
        'silencertfbs_set',
        'silencertfbs_set__binding_site',
        'silencersnps_set',
        'silencersnps_set__snp',
        'silencerrecognitionfactors_set',
        'silencerrecognitionfactors_set__recognition_factor',
        'silencersamplerecognitionfactors_set',
        'silencersamplerecognitionfactors_set__recognition_factor',
        'silencercas9s_set',
        'silencercas9s_set__region',
    ).all()
    silencer_rows = [[
        silencer.silencer_id,
        silencer.region.chromosome,
        silencer.region.start,
        silencer.region.end,
        silencer.strand,
        silencer.score,
        silencer.sample.sample_id,
        silencer.sample.bio_sample_name,
        silencer.sample.tissue_type,
        silencer.sample.bio_sample_type,
        silencer.sample.species,
        silencer.sample.source,
        ';'.join([
            silencer_gene.gene_name + ':' +
            silencer_gene.strategy + '.' + silencer_gene.sub_strategy for silencer_gene in
            silencer.silencergenes_set.all()
        ]),
        ';'.join([
            silencer_tfb.transcription_factor + '~' +
            silencer_tfb.binding_site.loci for silencer_tfb in silencer.silencertfbs_set.all()
        ]),
        ';'.join([
            silencer_snp.snp.rs_id + ':' +
            silencer_snp.variant for silencer_snp in silencer.silencersnps_set.all()
        ]),
        ';'.join([silencer_recognition_factor.recognition_factor.name
                  for silencer_recognition_factor in silencer.silencerrecognitionfactors_set.all()]),
        ';'.join([
            silencer_sample_recognition_factor.bio_sample_name + '-' +
            silencer_sample_recognition_factor.recognition_factor.name + '-' +
            str(int(silencer_sample_recognition_factor.recoginized)) + ':' +
            str(silencer_sample_recognition_factor.z_score)
            for silencer_sample_recognition_factor in silencer.silencersamplerecognitionfactors_set.all()
        ]),
        ';'.join([silencer_cas9.region.loci for silencer_cas9 in silencer.silencercas9s_set.all()])
    ] for silencer in silencers]

    pd.DataFrame(silencer_rows, columns=[
        'silencer_id',
        'chr',
        'start',
        'end',
        'strand',
        'score',
        'sample_id',
        'bio_sample_name',
        'tissue_cell_type',
        'bio_sample_type',
        'species',
        'source',
        'target_genes',
        'TFBs',
        'SNPs',
        'recognition_factors',
        'samples_recognition_factors_z_score',
        'cas9s',
    ]).to_csv(file_path, sep='\t')
    print('导出数据完成')


class Command(BaseCommand):
    help = 'silencer atlas database command'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--test', action='store_true', help='init database for testing')
        parser.add_argument('-i', '--init', action='store_true', help='init database base data')
        parser.add_argument('-b', '--build', action='store_true', help='build silencers')
        parser.add_argument('-p', '--pre_update', action='store_true', help='pre update silencers handler')
        parser.add_argument('-u', '--update', action='store_true', help='update rows in database')
        parser.add_argument('-d', '--delete', action='store_true',
                            help='delete rows in database, default is include method')
        parser.add_argument('-de', '--exclude', action='store_true', help='delete rows in database by exclude method')
        parser.add_argument('-da', '--delete_all', action='store_true', help='delete all rows in database')
        parser.add_argument('-e', '--export', action='store_true', help='export database to json')
        parser.add_argument('-f', '--file_path', type=str, help='data file path')
        parser.add_argument('-dir', '--dir_path', type=str,
                            help='init data directory path,default is SilencerAtlas/libs')

    def handle(self, *args, **options):
        test = options.get('test', False)
        delete_all = options.get('delete_all', False)
        build = options.get('build', None)
        if test:
            return init_test_database_data()
        elif delete_all:
            return delete_database_data_all()
        elif build:
            return build_database_data()
        else:
            init = options.get('init', False)
            pre_update = options.get('pre_update', None)
            update = options.get('update', False)
            delete = options.get('delete', False)
            exclude = options.get('exclude', False)
            export = options.get('export', False)
            file_path = options.get('file_path', None)
            dir_path = options.get('dir_path', None)
            if not file_path and not init:
                print('Please input file path')
                return
            if [init, pre_update, update, delete, export].count(True) == 0:
                print('Please choose an operation: -i or -a or -u or -d or -e')
                return
            if [init, pre_update, update, delete, export].count(True) > 1:
                print('Please confirm your operation. Choose one from -i, -a, -u, -d, -e.')
                return
            if init:
                return init_database_data(dir_path)
            elif pre_update:
                return pre_update_database_data(file_path)
            elif update:
                return update_database_data(file_path)
            elif delete:
                if exclude:
                    return delete_database_data(file_path, False)
                else:
                    return delete_database_data(file_path, True)
            elif export:
                return export_database_data(file_path)
            else:
                print('Please choose an operation: -i or -a or -u or -d or -e')
