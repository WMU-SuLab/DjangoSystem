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
from SilencerAtlas.viewModels.gene import filter_genes_any
from SilencerAtlas.viewModels.recognition_factor import filter_recognition_factors_any
from SilencerAtlas.viewModels.region import divide_region, filter_regions_any
from SilencerAtlas.viewModels.sample import filter_samples_any
from SilencerAtlas.viewModels.silencer import filter_silencers_any
from SilencerAtlas.viewModels.snp import filter_snps_any
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
    if not dir_path:
        dir_path = os.path.join(settings.BASE_DIR, 'SilencerAtlas/libs')
    print('import recognition factors data')
    RecognitionFactor.objects.bulk_create([
        RecognitionFactor(name=name)
        for name in recognition_factors.keys()], batch_size=1000,
        ignore_conflicts=True)
    # 初始化基因数据
    print('import gene data')
    genes_df = pd.read_csv(os.path.join(dir_path, 'Homo_sapiens.GRCh38.95.gene.bed'),
                           sep='\t', names=['chr', 'start', 'end', 'strand', 'ensembl_id', 'gene_symbol', 'bio_type'])
    regions_df = genes_df[['chr', 'start', 'end', ]]
    Region.objects.bulk_create([Region(
        chromosome='chr' + row['chr'],
        start=row['start'],
        end=row['end'],
    ) for index, row in regions_df.iterrows()], batch_size=1000,
        ignore_conflicts=True)
    Gene.objects.bulk_create([Gene(
        name=row['gene_symbol'],
        ensembl_id=row['ensembl_id'],
        region=Region.objects.get(chromosome='chr' + row['chr'], start=row['start'], end=row['end']),
        strand=row['strand'],
        bio_type=row['bio_type']
    ) for index, row in genes_df.iterrows()], batch_size=1000,
        ignore_conflicts=True)
    # 初始化基因样本数据
    print('import gene expressions data')
    # 样本名称对应表
    samples_ensembl_id = pd.read_csv(
        os.path.join(dir_path, 'GTEx_Analysis_v8_Annotations.Sample.Attributes.txt'),
        sep='\t', )
    samples_name = {row['SAMPID']: row['SMTSD'] for index, row in samples_ensembl_id.iterrows()}
    # 基因在各个样本中的表达数据
    gene_expressions_count = 0
    for gene_sample_expressions_df in pd.read_csv(
            os.path.join(dir_path, 'GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct'),
            # 这个文件比较大，必须分开读取；因为文件前两行没有用所以跳过，大约5万多行
            chunksize=1000, sep='\t', skiprows=2):
        gene_expressions_count += 1
        print(f'read gene_expressions {(gene_expressions_count - 1) * 1000 + 1}-{gene_expressions_count * 1000}')
        gene_names = gene_sample_expressions_df['Description'].tolist()
        print('bulk create gene')
        Gene.objects.bulk_create([Gene(name=name) for name in gene_names], batch_size=1000, ignore_conflicts=True)
        genes = Gene.objects.filter(name__in=gene_names)
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
                gene=filter_genes_any(genes, gene_name),
                bio_sample_name=bio_sample_name,
                expression_value=value,
            ) for gene_name, sample_expression in gene_samples.items() for bio_sample_name, value in
                sample_expression.items()],
            batch_size=1000,
            ignore_conflicts=True
        )
    # 初始化snp数据

    # 初始化Cas9数据
    print('初始化数据完成')


@print_accurate_execute_time
def update_database_data(file_path):
    count = 0
    for df in pd.read_csv(file_path, sep='\t', chunksize=100000):
        count += 1
        print(f'reading {(count - 1) * 100000 + 1}-{count * 100000} rows')
        # 构建区域数据
        print('building regions')
        chromosomes = [row['chr'].lower() for index, row in df.iterrows()]
        starts = [row['start'] for index, row in df.iterrows()]
        ends = [row['end'] for index, row in df.iterrows()]
        Region.objects.bulk_create([Region(
            chromosome=row['chr'].lower(),
            start=row['start'],
            end=row['end'],
        ) for index, row in df.iterrows()], batch_size=1000, ignore_conflicts=True)
        regions = Region.objects.filter(chromosome__in=chromosomes, start__in=starts, end__in=ends)
        # 构建样本数据
        print('building samples')
        sample_column = ['bio_sample_name', 'tissue_cell_type', 'bio_sample_type', ]
        if 'sample_id' in df.columns:
            sample_column.append('sample_id')
        if 'species' in df.columns:
            sample_column.append('species')
        if 'source' in df.columns:
            sample_column.append('source')
        samples_df = df[sample_column].drop_duplicates()
        Sample.objects.bulk_create([Sample(
            sample_id=row.get('sample_id', ''),
            bio_sample_name=row['bio_sample_name'],
            tissue_type=row['tissue_cell_type'],
            bio_sample_type=row['bio_sample_type'].lower(),
            species=row.get('species', 'human').lower(),
            source=row.get('source', 'encode').lower(),
        ) for index, row in samples_df.iterrows()], batch_size=1000, ignore_conflicts=True)
        bio_sample_names = [row['bio_sample_name'] for index, row in samples_df.iterrows()]
        samples = Sample.objects.filter(bio_sample_name__in=bio_sample_names)
        # 构建silencer基础数据
        print('building silencers')
        Silencer.objects.bulk_create([Silencer(
            silencer_id=row['silencer_id'],
            silencer_name=row.get('silencer_name', ''),
            region=filter_regions_any(regions, chromosome=row['chr'].lower(), start=row['start'], end=row['end']),
            strand=row.get('strand', '.'),
            score=row.get('score', 0),
            sample=filter_samples_any(samples, bio_sample_name=row['bio_sample_name']),
        ) for index, row in df.iterrows()], batch_size=1000, ignore_conflicts=True)
        silencer_ids = [row['silencer_id'] for index, row in df.iterrows()]
        print('deleting silencers related data')
        silencers = Silencer.objects.filter(silencer_id__in=silencer_ids)
        SilencerGenes.objects.filter(silencer__in=silencers).delete()
        SilencerTFBs.objects.filter(silencer__in=silencers).delete()
        SilencerSNPs.objects.filter(silencer__in=silencers).delete()
        SilencerRecognitionFactors.objects.filter(silencer__in=silencers).delete()
        SilencerSampleRecognitionFactors.objects.filter(silencer__in=silencers).delete()
        SilencerCas9s.objects.filter(silencer__in=silencers).delete()
        # 构建靶基因数据
        if 'target_genes' in df.columns:
            print('building target genes')
            silencer_genes = df['target_genes']
            gene_names = [gene_symbol for index, value in silencer_genes.items() for gene_symbol, strategy in
                          map(lambda item: item.split(':'), value.split(';'))]
            Gene.objects.bulk_create([Gene(name=name) for name in gene_names], batch_size=1000, ignore_conflicts=True)
            genes = Gene.objects.filter(name__in=gene_names)
            SilencerGenes.objects.bulk_create([SilencerGenes(
                silencer=filter_silencers_any(silencers, silencer_id=silencer_ids[index]),
                gene=filter_genes_any(genes, name=gene_symbol),
                strategy=strategy.lower()
            ) for index, value in silencer_genes.items()
                for gene_symbol, strategy in map(lambda item: item.split(':'), value.split(';'))], batch_size=1000)
        # 构建TFBs数据
        if 'TFBs' in df.columns:
            print('building TFBs')
            silencer_tfbs = df['TFBs']
            gene_names = [gene_symbol for index, value in silencer_tfbs.items() for gene_symbol in
                          map(lambda item: item.split('~')[0], value.split(';'))]
            Gene.objects.bulk_create([Gene(name=name) for name in gene_names], batch_size=1000, ignore_conflicts=True)
            genes = Gene.objects.filter(name__in=gene_names)
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
            Region.objects.bulk_create(
                [Region(chromosome=chromosome, start=start, end=end) for chromosome, start, end in locations],
                batch_size=1000, ignore_conflicts=True)
            regions = Region.objects.filter(chromosome__in=chromosomes, start__in=starts, end__in=ends)
            SilencerTFBs.objects.bulk_create([SilencerTFBs(
                silencer=filter_silencers_any(silencers, silencer_id=silencer_ids[index]),
                transcription_factor=filter_genes_any(genes, name=gene_symbol),
                binding_site=filter_regions_any(regions, chromosome=binding_site[0], start=binding_site[1],
                                                end=binding_site[2]),
            ) for index, value in silencer_tfbs.items()
                for gene_symbol, binding_site in
                map(lambda item: (item.split('~')[0], divide_region(item.split('~')[1])), value.split(';'))],
                batch_size=1000, )
        # 构建SNPs数据
        if 'SNPs' in df.columns:
            print('building SNPs')
            silencer_snps = df['SNPs']
            rs_ids = [rs_id for index, value in silencer_snps.items()
                      for rs_id, variant in map(lambda item: item.split(':'), value.split(';'))]
            SNP.objects.bulk_create([SNP(rs_id=rs_id) for rs_id in rs_ids], batch_size=1000, ignore_conflicts=True)
            snps = SNP.objects.filter(rs_id__in=rs_ids)
            SilencerSNPs.objects.bulk_create([SilencerSNPs(
                silencer=filter_silencers_any(silencers, silencer_id=silencer_ids[index]),
                snp=filter_snps_any(snps, rs_id=rs_id),
                variant=variant.lower(),
            ) for index, value in silencer_snps.items()
                for rs_id, variant in map(lambda item: item.split(':'), value.split(';'))], batch_size=1000, )
        # 构建Recognition Factors数据
        if 'recognition_factors' in df.columns:
            print('building recognition factors')
            silencer_recognition_factors = df['recognition_factors']
            recognition_factors_all = RecognitionFactor.objects.all()
            SilencerRecognitionFactors.objects.bulk_create([SilencerRecognitionFactors(
                silencer=filter_silencers_any(silencers, silencer_id=silencer_ids[index]),
                recognition_factor=filter_recognition_factors_any(recognition_factors_all,
                                                                  name=recognition_factor.lower())
            ) for index, value in silencer_recognition_factors.items() for recognition_factor in value.split(';')],
                batch_size=1000, )
        if 'samples_recognition_factors_z_score' in df.columns:
            print('building sample recognition factors z_score')
            silencer_sample_recognition_factors = df['samples_recognition_factors_z_score']
            recognition_factors_all = RecognitionFactor.objects.all()
            SilencerSampleRecognitionFactors.objects.bulk_create([SilencerSampleRecognitionFactors(
                silencer=filter_silencers_any(silencers, silencer_id=silencer_ids[index]),
                recognition_factor=filter_recognition_factors_any(recognition_factors_all,
                                                                  name=recognition_factor.lower()),
                bio_sample_name=bio_sample_name,
                z_score=float(z_score),
                recognized=bool(recognized),
            ) for index, value in silencer_sample_recognition_factors.items() for
                bio_sample_name, recognition_factor, recognized, z_score in
                map(lambda item: (*item.split(':')[0].split('-'), item.split(':')[1]), value.split(';'))],
                batch_size=1000, )
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
            Region.objects.bulk_create(
                [Region(chromosome=chromosome, start=start, end=end) for chromosome, start, end in locations],
                batch_size=1000, ignore_conflicts=True)
            regions = Region.objects.filter(chromosome__in=chromosomes, start__in=starts, end__in=ends)
            SilencerCas9s.objects.bulk_create([SilencerCas9s(
                silencer=filter_silencers_any(silencers, silencer_id=silencer_ids[index]),
                region=filter_regions_any(regions, chromosome, start, end)
            ) for index, value in silencer_cas9s.items() for chromosome, start, end in
                map(lambda item: divide_region(item), value.split(';'))], batch_size=1000, )
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


@print_accurate_execute_time
def export_database_data(file_path):
    silencers = Silencer.objects.prefetch_related(
        'region',
        'sample',
        'silencergenes_set',
        'silencergenes_set__gene',
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
            silencer_gene.gene.name + ':' +
            silencer_gene.strategy for silencer_gene in silencer.silencergenes_set.all()
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
        parser.add_argument('-u', '--update', action='store_true', help='update rows in database')
        parser.add_argument('-d', '--delete', action='store_true',
                            help='delete rows in database, default is include method')
        parser.add_argument('-de', '--exclude', action='store_true', help='delete rows in database by exclude method')
        parser.add_argument('-e', '--export', action='store_true', help='export database to json')
        parser.add_argument('-f', '--file_path', type=str, help='data file path')
        parser.add_argument('-dir', '--dir_path', type=str,
                            help='init data directory path,default is SilencerAtlas/libs')

    def handle(self, *args, **options):
        test = options.get('test', False)
        if test:
            return init_test_database_data()
        else:
            init = options.get('init', False)
            update = options.get('update', False)
            delete = options.get('delete', False)
            exclude = options.get('exclude', False)
            export = options.get('export', False)
            file_path = options.get('file_path', None)
            dir_path = options.get('dir_path', None)
            if not file_path and not init:
                print('Please input file path')
                return
            if [init, update, delete, export].count(True) == 0:
                print('Please choose an operation: -i or -a or -u or -d or -e')
                return
            if [init, update, delete, export].count(True) > 1:
                print('Please confirm your operation. Choose one from -i, -a, -u, -d, -e.')
                return
            if init:
                return init_database_data(dir_path)
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
