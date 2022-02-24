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
from collections import defaultdict
import os

import pandas as pd
from django.conf import settings
from django.db.models import Q

from SilencerAtlas.libs.model_choices import recognition_factors
from SilencerAtlas.models.gene import Gene, GeneRegion,GeneExpression
from SilencerAtlas.models.recognition_factor import RecognitionFactor
from SilencerAtlas.models.region import CommonRegion
from SilencerAtlas.models.sample import Sample
from SilencerAtlas.models.silencer import Silencer, SilencerRecognitionFactor, SilencerSampleRecognitionFactor, \
    SilencerSNP, SilencerTranscriptionFactor, \
    SilencerGene, SilencerCas9
from SilencerAtlas.models.snp import SNP
from SilencerAtlas.viewModels.gene import to_genes_dict
from SilencerAtlas.viewModels.recognition_factor import to_recognition_factors_dict
from SilencerAtlas.viewModels.region import divide_region, generate_region, to_regions_dict
from SilencerAtlas.viewModels.sample import to_samples_dict
from SilencerAtlas.viewModels.snp import to_snps_dict
from utils.command import BaseCommand
from utils.file_handler.table_handler.csv import read_csv_n_lines_each_time_by_pandas_yield
from utils.time import print_accurate_execute_time


@print_accurate_execute_time
def init_database_data(dir_path, chunk_size=1000):
    """
    测试花费时间：80分钟
    初始化数据：包括识别因子数据，基因数据，基因表达数据，snp数据，Cas9
    :param batch_size:
    :param skip_rows:
    :param chunk_size:
    :param dir_path:
    :return:
    """
    # 先初始化识别因子的数据
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
    print('build regions')
    CommonRegion.objects.bulk_create([CommonRegion(
        chromosome='chr'+row['chr'],
        start=row['start'],
        end=row['end']
    )for index,row in genes_df.iterrows()], batch_size=batch_size, ignore_conflicts=True)
    chromosomes=('chr'+genes_df['chr'].drop_duplicates()).to_list()
    starts=genes_df['start'].drop_duplicates().to_list()
    ends=genes_df['end'].drop_duplicates().to_list()
    regions=to_regions_dict(list(CommonRegion.objects.filter(chromosome__in=chromosomes).filter(Q(start__in=starts)|Q(end__in=ends))))
    print('build genes')
    Gene.objects.bulk_create([Gene(
        name=row['gene_symbol'],
        ensembl_id=row['ensembl_id'],
        strand=row['strand'],
        bio_type=row['bio_type']
    ) for index, row in genes_df.iterrows()], batch_size=batch_size, ignore_conflicts=True)
    genes = to_genes_dict(list(Gene.objects.all()))
    print('build gene regions')
    GeneRegion.objects.bulk_create([GeneRegion(
        gene=genes[row['gene_symbol']],
        region=regions[generate_region(chromosome='chr' + row['chr'], start=row['start'], end=row['end'])]
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
            chunk_size=chunk_size, skip_rows=2,has_header=False):
        gene_names = gene_sample_expressions_df['Description'].drop_duplicates().tolist()
        bio_sample_names=[]
        print('bulk create gene')
        gene_sample_expressions = {}
        for index, row in gene_sample_expressions_df.iterrows():
            gene_name=row['Description']
            sample_expression = defaultdict(list)
            for col_name, value in row[2:].iteritems():
                bio_sample_name=samples_name[col_name]
                bio_sample_names.append(bio_sample_name)
                sample_expression[bio_sample_name].append(value)
            gene_sample_expressions[gene_name] = sample_expression
        print('bulk create gene expressions')
        GeneExpression.objects.bulk_create(
            [GeneExpression(
                gene_name=gene_name,
                bio_sample_name=bio_sample_name,
            ) for gene_name, sample_expression in gene_sample_expressions.items() for bio_sample_name, value in
                sample_expression.items()],
            batch_size=batch_size,
            ignore_conflicts=True
        )
        gene_expressions=GeneExpression.objects.filter(gene_name__in=gene_names,bio_sample_name__in=bio_sample_names)
        for gene_expression in gene_expressions:
            gene_expression.expression_value=gene_sample_expressions[gene_expression.gene_name][gene_expression.bio_sample_name]
        GeneExpression.objects.bulk_update(gene_expressions, ['expression_value'], batch_size=batch_size)
    # todo:补全剩余数据
    # 初始化snp数据

    # 初始化Cas9数据

    print('初始化数据完成')


@print_accurate_execute_time
def pre_update_database_data(file_path, chunk_size=10000, skip_rows=0):
    batch_size = 10000
    for df in read_csv_n_lines_each_time_by_pandas_yield(file_path, sep='\t', chunk_size=chunk_size,
                                                         skip_rows=skip_rows):
        silencer_ids = df['silencer_id'].to_list()
        print('building silencers')
        Silencer.objects.bulk_create([Silencer(
            silencer_id=silencer_id,
        ) for silencer_id in silencer_ids], batch_size=batch_size, ignore_conflicts=True)
        print('building samples')
        columns = df.columns.to_list()
        if 'bio_sample_name' not in columns:
            print('no bio_sample_name')
            return
        sample_column = list(
            {'sample_id', 'bio_sample_name', 'tissue_cell_type', 'bio_sample_type', 'species', 'source'} & set(columns))
        bio_sample_names = df['bio_sample_name'].drop_duplicates().to_list()
        samples_df = df[sample_column].drop_duplicates()
        Sample.objects.bulk_create([Sample(
            bio_sample_name=bio_sample_name,
        ) for bio_sample_name in bio_sample_names], batch_size=batch_size,ignore_conflicts=True)
        samples = to_samples_dict(list(Sample.objects.filter(bio_sample_name__in=bio_sample_names)))
        print('update samples')
        new_samples = []
        for index, row in samples_df.iterrows():
            sample = samples[row['bio_sample_name']]
            sample.sample_id = row.get('sample_id', '')
            sample.tissue_type = row.get('tissue_type', row['bio_sample_name'])
            sample.bio_sample_type = row['bio_sample_type'].lower()
            sample.species = row.get('species', 'human').lower()
            sample.source = row.get('source', 'encode').lower()
            new_samples.append(sample)
        Sample.objects.bulk_update(new_samples,
                                   fields=['sample_id', 'tissue_type', 'bio_sample_type', 'species', 'source'],
                                   batch_size=batch_size)


@print_accurate_execute_time
def update_database_data(file_path, chunk_size=10000, skip_rows=0):
    batch_size = 1000
    for df in read_csv_n_lines_each_time_by_pandas_yield(file_path, sep='\t', chunk_size=chunk_size,
                                                         skip_rows=skip_rows):
        # 构建区域数据
        print('building regions')
        chromosomes = df['chr'].drop_duplicates().str.lower().to_list()
        starts = df['start'].drop_duplicates().to_list()
        ends = df['end'].drop_duplicates().to_list()
        CommonRegion.objects.bulk_create([CommonRegion(
            chromosome=row['chr'].lower(),
            start=row['start'],
            end=row['end'],
        ) for index, row in df.iterrows()], batch_size=batch_size, ignore_conflicts=True)
        regions = to_regions_dict(
            list(CommonRegion.objects.filter(chromosome__in=chromosomes).filter(Q(start__in=starts) | Q(end__in=ends))))
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
        SilencerGene.objects.filter(silencer__in=silencers).delete()
        SilencerTranscriptionFactor.objects.filter(silencer__in=silencers).delete()
        SilencerSNP.objects.filter(silencer__in=silencers).delete()
        SilencerRecognitionFactor.objects.filter(silencer__in=silencers).delete()
        SilencerSampleRecognitionFactor.objects.filter(silencer__in=silencers).delete()
        SilencerCas9.objects.filter(silencer__in=silencers).delete()
        # 构建靶基因数据
        if 'target_genes' in df.columns:
            print('building target genes')
            target_genes = df['target_genes']
            silencer_genes_to_create=[]
            for index, value in target_genes.items():
                silencer_genes=value.split(';')
                for silencer_gene in silencer_genes:
                    gene,strategies=silencer_gene.split(':')
                    gene_name,gene_ensembl_id,genomic_loci,distance=gene.split('~')
                    strategy,sub_strategy=strategies.split('.')
                    silencer_genes_to_create.append(SilencerGene(
                        silencer=silencers[index % chunk_size],
                        gene_name=gene_name,
                        gene_ensembl_id=gene_ensembl_id,
                        genomic_loci=genomic_loci,
                        distance_to_TSS=distance,
                        strategy=strategy.lower(),
                        sub_strategy=sub_strategy,
                    ))
            SilencerGene.objects.bulk_create(silencer_genes_to_create,batch_size=1000, ignore_conflicts=True)
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
            CommonRegion.objects.bulk_create(
                [CommonRegion(chromosome=chromosome, start=start, end=end) for chromosome, start, end in locations],
                batch_size=batch_size, ignore_conflicts=True)
            regions = to_regions_dict(
                list(CommonRegion.objects.filter(chromosome__in=chromosomes).filter(
                    Q(start__in=starts) | Q(end__in=ends))))
            SilencerTranscriptionFactor.objects.bulk_create([SilencerTranscriptionFactor(
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
            SilencerSNP.objects.bulk_create([SilencerSNP(
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
            SilencerRecognitionFactor.objects.bulk_create([SilencerRecognitionFactor(
                silencer=silencers[index % chunk_size],
                recognition_factor=recognition_factors_all[recognition_factor.lower()],
            ) for index, value in silencer_recognition_factors.items() for recognition_factor in value.split(';')],
                batch_size=batch_size, ignore_conflicts=True)
        if 'samples_recognition_factors_z_score' in df.columns:
            print('building sample recognition factors z_score')
            silencer_sample_recognition_factors = df['samples_recognition_factors_z_score']
            recognition_factors_all = to_recognition_factors_dict(list(RecognitionFactor.objects.all()))
            SilencerSampleRecognitionFactor.objects.bulk_create([SilencerSampleRecognitionFactor(
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
            CommonRegion.objects.bulk_create(
                [CommonRegion(chromosome=chromosome, start=start, end=end) for chromosome, start, end in locations],
                batch_size=batch_size, ignore_conflicts=True)
            regions = to_regions_dict(
                list(CommonRegion.objects.filter(chromosome__in=chromosomes).filter(
                    Q(start__in=starts) | Q(end__in=ends))))
            SilencerCas9.objects.bulk_create([SilencerCas9(
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
    # todo:导出数据等待数据库全部完成后在重新调整
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
        parser.add_argument('-i', '--init', action='store_true', help='init database base data')
        parser.add_argument('-p', '--pre_update', action='store_true', help='pre update silencers handler')
        parser.add_argument('-u', '--update', action='store_true', help='update rows in database')
        parser.add_argument('-d', '--delete', action='store_true',
                            help='delete rows in database, default is include method')
        parser.add_argument('-de', '--exclude', action='store_true', help='delete rows in database by exclude method')
        parser.add_argument('-da', '--delete_all', action='store_true', help='delete all rows in database')
        parser.add_argument('-e', '--export', action='store_true', help='export database to json')
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        delete_all = options.get('delete_all', False)
        if delete_all:
            return delete_database_data_all()
        else:
            init = options.get('init', False)
            pre_update = options.get('pre_update', None)
            update = options.get('update', False)
            delete = options.get('delete', False)
            exclude = options.get('exclude', False)
            export = options.get('export', False)
            file_path = options.get('file_path', None)
            dir_path = options.get('dir_path', None)
            chunk_size = options.get('chunk_size', 0)
            skip_rows = options.get('skip_rows', 0)
            kargs = {}
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
                if chunk_size:
                    kargs['chunk_size'] = chunk_size
                return init_database_data(dir_path, **kargs)
            elif pre_update:
                if chunk_size:
                    kargs['chunk_size'] = chunk_size
                if skip_rows:
                    kargs['skip_rows'] = skip_rows
                return pre_update_database_data(file_path, **kargs)
            elif update:
                if chunk_size:
                    kargs['chunk_size'] = chunk_size
                if skip_rows:
                    kargs['skip_rows'] = skip_rows
                return update_database_data(file_path, **kargs)
            elif delete:
                if exclude:
                    return delete_database_data(file_path, False)
                else:
                    return delete_database_data(file_path, True)
            elif export:
                return export_database_data(file_path)
            else:
                print('Please choose an operation: -i or -a or -u or -d or -e')
