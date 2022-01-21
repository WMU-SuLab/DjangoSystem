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

import pandas as pd
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
from SilencerAtlas.viewModels.region import divide_region
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
    print('import recognition factors data')
    RecognitionFactor.objects.bulk_create([
        RecognitionFactor(name=name)
        for name in recognition_factors.keys()], ignore_conflicts=True)
    # 初始化基因数据
    print('import gene data')
    genes_df = pd.read_csv('D:\Coding\Python\Django-backend\System\SilencerAtlas\libs\Homo_sapiens.GRCh38.95.gene.bed',
                           sep='\t', names=['chr', 'start', 'end', 'strand', 'ensembl_id', 'gene_symbol', 'bio_type'])
    regions_df = genes_df[['chr', 'start', 'end', ]]
    Region.objects.bulk_create([Region(
        chromosome='chr' + row['chr'],
        start=row['start'],
        end=row['end'],
    ) for index, row in regions_df.iterrows()], ignore_conflicts=True)
    Gene.objects.bulk_create([Gene(
        name=row['gene_symbol'],
        ensembl_id=row['ensembl_id'],
        region=Region.objects.get(chromosome='chr' + row['chr'], start=row['start'], end=row['end']),
        strand=row['strand'],
        bio_type=row['bio_type']
    ) for index, row in genes_df.iterrows()], ignore_conflicts=True)
    # 初始化基因样本数据
    print('import gene expressions data')
    # 样本名称对应表
    samples_ensembl_id = pd.read_csv(
        'D:\Coding\Python\Django-backend\System\SilencerAtlas\libs\GTEx_Analysis_v8_Annotations.Sample.Attributes.txt',
        sep='\t', )
    samples_name = {row['SAMPID']: row['SMTSD'] for index, row in samples_ensembl_id.iterrows()}
    # 基因在各个样本中的表达数据
    gene_expressions_count = 0
    for gene_sample_expressions_df in pd.read_csv(
            'D:\Coding\Python\Django-backend\System\SilencerAtlas\libs\GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct',
            # 这个文件比较大，必须分开读取；因为文件前两行没有用所以跳过，大约5万多行
            chunksize=1000, sep='\t', skiprows=2):
        gene_expressions_count += 1
        print(f'read gene_expressions {(gene_expressions_count - 1) * 1000}-{gene_expressions_count * 1000}')
        for index, row in gene_sample_expressions_df.iterrows():
            gene, gene_created = Gene.objects.get_or_create(name=row['Description'])
            gene_expression = {}
            for col_name, value in row[2:].iteritems():
                if gene_expression.get(samples_name[col_name], None):
                    gene_expression[samples_name[col_name]] += [value]
                else:
                    gene_expression[samples_name[col_name]] = [value]
            GeneExpression.objects.bulk_create(
                [GeneExpression(
                    gene=gene,
                    bio_sample_name=bio_sample_name,
                    expression_value=value,
                ) for bio_sample_name, value in gene_expression.items()],
                ignore_conflicts=True
            )
    # 初始化snp数据

    # 初始化Cas9数据
    print('初始化数据完成')


@print_accurate_execute_time
def add_database_data(file_path):
    for df in pd.read_csv(file_path, chunksize=100000):
        silencers_df = df[['silencer_id', 'chr', 'start', 'end', 'strand', 'score']]
        # 构建区域数据
        regions = Region.objects.bulk_create([Region(
            chromosome=row['chr'],
            start=row['start'],
            end=row['end'],
        ) for index, row in silencers_df.iterrows()])
        samples_df = df[['sample_id', 'bio_sample_name', 'tissue_cell_type', 'bio_sample_type', 'species',
                         'source']].drop_duplicates()
        # 构建样本数据
        samples = Sample.objects.bulk_create([Sample(
            sample_id=row.get('sample_id', ''),
            bio_sample_name=row['bio_sample_name'],
            tissue_type=row['tissue_cell_type'],
            bio_sample_type=row['bio_sample_type'],
            species=row['species'],
            source=row['source'],
        ) for index, row in samples_df.iterrows()])
        # 构建silencer基础数据
        silencers = Silencer.objects.bulk_create([Silencer(
            silencer_id=row['silencer_id'],
            silencer_name=row.get('silencer_name', ''),
            region=regions[index],
            strand=row['strand'],
            score=row['score'],
            sample=samples[index],
        ) for index, row in silencers_df.iterrows()])
        # 构建靶基因数据
        silencer_genes = df['target_genes']
        SilencerGenes.objects.bulk_create(*[SilencerGenes(
            silencer=silencers[index],
            gene=Gene.objects.get_or_create(name=gene_symbol)[0],
            strategy=strategy.lower()
        ) for index, value in silencer_genes.items()
            for gene_symbol, strategy in map(lambda item: item.split(':'), value.split(';'))])
        # 构建TFBs数据
        silencer_tfbs = df['TFBs']
        SilencerTFBs.objects.bulk_create([SilencerTFBs(
            silencer=silencers[index],
            transcription_factor=Gene.objects.get_or_create(name=gene_symbol)[0],
            binding_site=
            Region.objects.get_or_create(chromosome=binding_site[0], start=binding_site[1], end=binding_site[2])[0],
        ) for index, value in silencer_tfbs.items()
            for gene_symbol, binding_site in
            map(lambda item: (item.split('~')[0], divide_region(item.split('~')[1])), value.split(';'))])
        # 构建SNPs数据
        silencer_snps = df['SNPs']
        SilencerSNPs.objects.bulk_create([SilencerSNPs(
            silencer=silencers[index],
            snp=SNP.objects.get_or_create(rs_id=rs_id)[0],
            variant=variant.lower(),
        ) for index, value in silencer_snps.items()
            for rs_id, variant in map(lambda item: item.split(':'), value.split(';'))])
        # 构建Recognition Factors数据
        silencer_recognition_factors = df['recognition_factors']
        SilencerRecognitionFactors.objects.bulk_create([SilencerRecognitionFactors(
            silencer=silencers[index],
            recognition_factor=RecognitionFactor.objects.get(name=recognition_factor.lower())
        ) for index, value in silencer_recognition_factors.items() for recognition_factor in value.split(';')])
        silencer_sample_recognition_factors = df['samples_z_score']
        SilencerSampleRecognitionFactors.objects.bulk_create([SilencerSampleRecognitionFactors(
            silencer=silencers[index],
            recognition_factor=RecognitionFactor.objects.get(name=recognition_factor.lower()),
            bio_sample_name=bio_sample_name,
            z_score=float(z_score),
            recognized=bool(recognized),
        ) for index, value in silencer_sample_recognition_factors.items() for
            bio_sample_name, recognition_factor, recognized, z_score in
            map(lambda item: (*item.split(':')[0].split('-'), item.split(':')[1]), value.split(';'))])
        # 构建Cas9数据
        silencer_cas9s = df['Cas9s']
        SilencerCas9s.objects.bulk_create([SilencerCas9s(
            silencer=silencers[index],
            region=Region.objects.get_or_create(chromosome=chromosome, start=start, end=end)
        ) for index, value in silencer_cas9s.items() for chromosome, start, end in
            map(lambda item: divide_region(item), value.split(';'))])

    print('添加数据完成')


@print_accurate_execute_time
def update_database_data(file_path):
    for df in pd.read_csv(file_path, chunksize=10000):
        silencers_df = df[['silencer_id', 'chr', 'start', 'end', 'strand', 'score']]
        # 构建区域数据
        Region.objects.bulk_create(*[Region(
            chromosome=row['chr'],
            start=row['start'],
            end=row['end'],
        ) for index, row in silencers_df.iterrows()])
        samples_df = df[['sample_id', 'bio_sample_name', 'tissue_cell_type', 'bio_sample_type', 'species',
                         'source']].drop_duplicates()
        # 构建样本数据
        Sample.objects.bulk_create(*[Sample(
            sample_id=row['sample_id'],
            bio_sample_name=row['bio_sample_name'],
            tissue_type=row['tissue_cell_type'],
            bio_sample_type=row['bio_sample_type'],
            species=row['species'],
            source=row['source'],
        ) for index, row in samples_df.iterrows()])
        # 构建silencer基础数据
        silencers = Silencer.objects.bulk_create(*[Silencer(
            silencer_id=row['silencer_id'],
            region=Region.objects.get(chromosome=row['chr'], start=row['start'], end=row['end']),
            strand=row['strand'],
            score=row['score'],
            sample=Sample.objects.get(bio_sample_name=row['sample_id']),
        ) for index, row in silencers_df.iterrows()])
        for silencer in silencers:
            silencer.save()
            SilencerGenes.objects.filter(silencer=silencer).delete()
            SilencerTFBs.objects.filter(silencer=silencer).delete()
            SilencerSNPs.objects.filter(silencer=silencer).delete()
            SilencerRecognitionFactors.objects.filter(silencer=silencer).delete()
            SilencerSampleRecognitionFactors.objects.filter(silencer=silencer).delete()
            SilencerCas9s.objects.filter(silencer=silencer).delete()
        # 构建靶基因数据
        silencer_genes = df['target_genes']
        SilencerGenes.objects.bulk_create(*[SilencerGenes(
            silencer=silencers[index],
            gene=Gene.objects.get_or_create(name=gene_symbol)[0],
            strategy=strategy.lower()
        ) for index, value in silencer_genes.items()
            for gene_symbol, strategy in map(lambda item: item.split(':'), value.split(';'))])
        # 构建TFBs数据
        silencer_tfbs = df['TFBs']
        SilencerTFBs.objects.bulk_create([SilencerTFBs(
            silencer=silencers[index],
            transcription_factor=Gene.objects.get_or_create(name=gene_symbol)[0],
            binding_site=
            Region.objects.get_or_create(chromosome=binding_site[0], start=binding_site[1], end=binding_site[2])[0],
        ) for index, value in silencer_tfbs.items()
            for gene_symbol, binding_site in
            map(lambda item: (item.split('~')[0], divide_region(item.split('~')[1])), value.split(';'))])
        # 构建SNPs数据
        silencer_snps = df['SNPs']
        SilencerSNPs.objects.bulk_create([SilencerSNPs(
            silencer=silencers[index],
            snp=SNP.objects.get_or_create(rs_id=rs_id)[0],
            variant=variant.lower(),
        ) for index, value in silencer_snps.items()
            for rs_id, variant in map(lambda item: item.split(':'), value.split(';'))])
        # 构建Recognition Factors数据
        silencer_recognition_factors = df['recognition_factors']
        SilencerRecognitionFactors.objects.bulk_create([SilencerRecognitionFactors(
            silencer=silencers[index],
            recognition_factor=RecognitionFactor.objects.get(name=recognition_factor.lower())
        ) for index, value in silencer_recognition_factors.items() for recognition_factor in value.split(';')])
        silencer_sample_recognition_factors = df['samples_z_score']
        SilencerSampleRecognitionFactors.objects.bulk_create([SilencerSampleRecognitionFactors(
            silencer=silencers[index],
            recognition_factor=RecognitionFactor.objects.get(name=recognition_factor.lower()),
            bio_sample_name=bio_sample_name,
            z_score=float(z_score),
            recognized=bool(recognized),
        ) for index, value in silencer_sample_recognition_factors.items() for
            bio_sample_name, recognition_factor, recognized, z_score in
            map(lambda item: (*item.split(':')[0].split('-'), item.split(':')[1]), value.split(';'))])
        # 构建Cas9数据
        silencer_cas9s = df['Cas9s']
        SilencerCas9s.objects.bulk_create([SilencerCas9s(
            silencer=silencers[index],
            region=Region.objects.get_or_create(chromosome=chromosome, start=start, end=end)
        ) for index, value in silencer_cas9s.items() for chromosome, start, end in
            map(lambda item: divide_region(item), value.split(';'))])

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
        parser.add_argument('-a', '--add', action='store_true', help='add rows to database')
        parser.add_argument('-u', '--update', action='store_true', help='update rows in database')
        parser.add_argument('-d', '--delete', action='store_true',
                            help='delete rows in database, default is include method')
        parser.add_argument('-de', '--exclude', action='store_true', help='delete rows in database by exclude method')
        parser.add_argument('-e', '--export', action='store_true', help='export database to json')
        parser.add_argument('-f', '--file_or_dir_path', type=str, help='data file path or init data directory path')

    def handle(self, *args, **options):
        test = options.get('test', False)
        if test:
            return init_test_database_data()
        else:
            init = options.get('init', False)
            add = options.get('add', False)
            update = options.get('update', False)
            delete = options.get('delete', False)
            exclude = options.get('exclude', False)
            export = options.get('export', False)
            file_or_dir_path = options.get('file_or_dir_path', None)
            if not file_or_dir_path and not init:
                print('Please input file path')
                return
            if [init, add, update, delete, export].count(True) == 0:
                print('Please choose an operation: -i or -a or -u or -d or -e')
                return
            if [init, add, update, delete, export].count(True) > 1:
                print('Please confirm your operation. Choose one from -i, -a, -u, -d, -e.')
                return
            if init:
                return init_database_data(file_or_dir_path)
            elif add:
                return add_database_data(file_or_dir_path)
            elif update:
                return update_database_data(file_or_dir_path)
            elif delete:
                if exclude:
                    return delete_database_data(file_or_dir_path, False)
                else:
                    return delete_database_data(file_or_dir_path, True)
            elif export:
                return export_database_data(file_or_dir_path)
            else:
                print('Please choose an operation: -i or -a or -u or -d or -e')
