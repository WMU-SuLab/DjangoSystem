# -*- encoding: utf-8 -*-
"""
@File Name      :   silencer.py    
@Create Time    :   2021/12/28 19:30
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

import json
import time

from django.db.models import Count, Q, F
from django.views.decorators.http import require_POST, require_GET
from django_mysql.models import GroupConcat

from SilencerAtlas.libs.lists import unknown_value_list
from SilencerAtlas.models.gene import GeneExpression
from SilencerAtlas.models.sample import Sample
from SilencerAtlas.models.silencer import Silencer, SilencerSampleRecognitionFactor, SilencerGene
from SilencerAtlas.utils import remove_duplicate_dict_list
from SilencerAtlas.viewModels import handle_sort_order,handle_pagination
from SilencerAtlas.viewModels.recognition_factor import recognition_factors_upper
from SilencerAtlas.viewModels.region import divide_region
from SilencerAtlas.viewModels.silencer import filtered_unknown_silencers
from Common.utils.response import JsonResponse
from Common.utils.text_handler import lower_underline


@require_POST
def get_silencers(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    source = data.get('source', '')
    species = data.get('species', '')
    bio_sample_type = data.get('bioSampleType', '')
    # tissue_type = data.get('tissueType', '')
    # 按区域查询
    region = lower_underline(data.get('region', ''))
    # 按基因查询
    strategy = data.get('strategy', '')
    gene = data.get('gene', '')
    # 按转录因子查询
    transcription_factor = data.get('transcriptionFactor', '')
    # 按SNP查询
    rs_id = data.get('rsId', '')
    variant = data.get('variant', '')
    # 获得Silencer相关数据
    # silencers = filtered_unknown_silencers()
    silencers= Silencer.objects.all()
    if source:
        silencers = silencers.filter(sample__source=source)
    if species:
        silencers = silencers.filter(sample__species=species)
    if bio_sample_type:
        silencers = silencers.filter(sample__bio_sample_type=bio_sample_type)
    # if tissue_type:
    #     silencers = silencers.filter(sample__tissue_type=tissue_type)
    if region:
        chromosome, start, end = divide_region(region)
        # 对于输入范围的起始和终止位点，查询的silencer需要起始位点小于范围终止位点，终止位点大于范围起始位点（可能有点绕）
        silencers = silencers.filter(region__chromosome__icontains=chromosome, region__start__lte=int(end),
                                     region__end__gte=int(start))
    if gene:
        silencers = silencers.filter(target_genes__gene_name__icontains=gene)
    if strategy:
        silencers = silencers.filter(target_genes__strategy=strategy)
    if transcription_factor:
        silencers = silencers.filter(silencertranscriptionfactor__transcription_factor__name__icontains=transcription_factor)
    if rs_id:
        silencers = silencers.filter(silencersnp__snp__rs_id__icontains=rs_id)
    if variant:
        silencers = silencers.filter(silencersnp__variant=variant)
    # 根据查询条件过滤
    # 构建表格属性
    silencers = silencers.annotate(
        chromosome=F('region__chromosome'),
        start=F('region__start'),
        end=F('region__end'),
        # GroupConcat之后再链接其他多对多会导致多个左连接，需要在每一个上面去除重复值
        recognition_factors_group_concat=GroupConcat(
            'silencerrecognitionfactor__recognition_factor__name', distinct=True),
        eQTLs_count=Count('SNPs', Q(silencersnp__variant='eQTL'), distinct=True),
        risk_snps_count=Count('SNPs', Q(silencersnp__variant='risk_snp'), distinct=True),
        TFBs_count=Count('TFBs', distinct=True), Cas9s_count=Count('Cas9s', distinct=True)
    )
    # 先查询
    # 由于插件问题传过来的是字符串，需要转换成字典
    filters = data.get('filters', '')
    if filters:
        filters = json.loads(filters)
        silencer_id = filters.get('silencer_id', '')
        if silencer_id:
            silencers = silencers.filter(silencer_id__icontains=silencer_id)
        chromosome = filters.get('chromosome', '')
        if chromosome:
            silencers = silencers.filter(chromosome__icontains=chromosome)
        start = filters.get('start', '')
        if start:
            silencers = silencers.filter(start__icontains=start)
        end = filters.get('end', '')
        if end:
            silencers = silencers.filter(end__icontains=end)
        recognition_factors_group_concat = filters.get('recognition_factors', '')
        if recognition_factors_group_concat:
            silencers = silencers.filter(
                recognition_factors_group_concat__icontains=recognition_factors_group_concat)
        eQTLs_count = filters.get('eQTLs_count', '')
        if eQTLs_count or eQTLs_count == 0:
            silencers = silencers.filter(eQTLs_count__icontains=eQTLs_count)
        risk_snps_count = filters.get('risk_snps_count', '')
        if risk_snps_count or risk_snps_count == 0:
            silencers = silencers.filter(risk_snps_count__icontains=risk_snps_count)
        TFBs_count = filters.get('TFBs_count', '')
        if TFBs_count or TFBs_count == 0:
            silencers = silencers.filter(TFBs_count__icontains=TFBs_count)
        Cas9s_count = filters.get('Cas9s_count', '')
        if Cas9s_count or Cas9s_count == 0:
            silencers = silencers.filter(Cas9s_count__icontains=Cas9s_count)
    # 综合查询拥有更高的权限
    search_text = data.get('searchText', '')
    if search_text:
        silencers = silencers.filter(
            Q(silencer_id__icontains=search_text) | Q(chromosome__icontains=search_text) |
            Q(start__icontains=search_text) | Q(start__icontains=search_text) |
            Q(recognition_factors_group_concat__icontains=search_text) | Q(eQTLs_count__icontains=search_text) |
            Q(risk_snps_count__icontains=search_text) | Q(TFBs_count__icontains=search_text) |
            Q(Cas9s_count__icontains=search_text)
        )
    # 再排序
    silencers=handle_sort_order(data, silencers)
    # 再分页
    silencers_current_page,total,first_load=handle_pagination(data,Silencer, silencers)
    # 转为表格数据
    rows = [{
        'id': silencer.id, 'silencer_id': silencer.silencer_id, 'chromosome': silencer.chromosome,
        'start': silencer.start, 'end': silencer.end,
        'recognition_factors': recognition_factors_upper(silencer.recognition_factors_group_concat or '--'),
        'eQTLs_count': silencer.eQTLs_count, 'risk_snps_count': silencer.risk_snps_count,
        'TFBs_count': silencer.TFBs_count, 'Cas9s_count': silencer.Cas9s_count,
    } for silencer in silencers_current_page]
    return JsonResponse({'total':total,'rows': rows,'firstLoad':first_load})


@require_GET
def get_silencer_by_id(request, silencer_id):
    silencer = Silencer.objects.prefetch_related('sample').get(id=silencer_id)
    silencer_id = silencer.silencer_id
    # Signal In Specific Bio Samples
    signal_in_this_bio_sample = []
    silencer_sample_recognition_factors = SilencerSampleRecognitionFactor.objects.prefetch_related('silencer',
                                                                                                    'recognition_factor').filter(
        silencer__silencer_id=silencer_id,
        bio_sample_name__in=list(
            {silencer.sample.bio_sample_name, '_'.join(silencer.sample.bio_sample_name.split(' '))})
    ).exclude(recognition_factor__name__in=unknown_value_list)
    signal_in_this_bio_sample_row = {'bio_sample_name': silencer.sample.bio_sample_name, }
    recognition_factors_list = []
    for silencer_sample_recognition_factor in silencer_sample_recognition_factors:
        signal_in_this_bio_sample_row[
            silencer_sample_recognition_factor.recognition_factor.name] = silencer_sample_recognition_factor.z_score
        if silencer_sample_recognition_factor.recognized:
            recognition_factors_list.append(silencer_sample_recognition_factor.recognition_factor.get_name_display())
    signal_in_this_bio_sample_row['recognition_factors'] = ','.join(recognition_factors_list)
    signal_in_this_bio_sample.append(signal_in_this_bio_sample_row)

    signal_in_other_bio_samples = []
    other_bio_sample_names = list(
        SilencerSampleRecognitionFactor.objects.filter(silencer=silencer).exclude(
            bio_sample_name=silencer.sample.bio_sample_name).distinct().values_list('bio_sample_name', flat=True))
    for other_bio_sample_name in other_bio_sample_names:
        signal_in_other_bio_samples_row = {'bio_sample_name': other_bio_sample_name, }
        recognition_factors_list = []
        silencer_sample_recognition_factors = SilencerSampleRecognitionFactor.objects.filter(
            silencer__silencer_id=silencer_id,
            bio_sample_name__in=list({other_bio_sample_name, '_'.join(other_bio_sample_name.split(' '))})
        ).exclude(recognition_factor__name__in=unknown_value_list).prefetch_related('silencer','recognition_factor')
        for silencer_sample_recognition_factor in silencer_sample_recognition_factors:
            signal_in_other_bio_samples_row[
                silencer_sample_recognition_factor.recognition_factor.name] = silencer_sample_recognition_factor.z_score
            if silencer_sample_recognition_factor.recognized:
                recognition_factors_list.append(
                    silencer_sample_recognition_factor.recognition_factor.get_name_display())
        signal_in_other_bio_samples_row['recognition_factors'] = ','.join(recognition_factors_list)
        signal_in_other_bio_samples.append(signal_in_other_bio_samples_row)
    signal_in_specific_bio_samples_tables_data = {
        'signal_in_this_bio_sample': signal_in_this_bio_sample,
        'signal_in_other_bio_samples': signal_in_other_bio_samples
    }

    # Putative Target Gene
    # 表格
    silencer_genes = list(SilencerGene.objects.filter(silencer=silencer))
    putative_target_genes_table_data = [
        # {"strategies_algorithm": "Lasso"},
        # {"strategies_algorithm": "PreSTIGE"}
    ]
    putative_target_genes_table_data_dict = {}
    for silencer_gene in silencer_genes:
        strategy = silencer_gene.get_strategy_display()
        sub_strategy = silencer_gene.sub_strategy
        if strategy in putative_target_genes_table_data_dict:
            if sub_strategy:
                if sub_strategy in putative_target_genes_table_data_dict[strategy]:
                    putative_target_genes_table_data_dict[strategy][sub_strategy]['gene_name'].append(silencer_gene.gene_name)
                    putative_target_genes_table_data_dict[strategy][sub_strategy]['gene_ensembl_id'].append(
                        silencer_gene.gene_ensembl_id)
                    putative_target_genes_table_data_dict[strategy][sub_strategy]['genomic_loci'].append(silencer_gene.genomic_loci)
                    putative_target_genes_table_data_dict[strategy][sub_strategy]['distance_to_TSS'].append(
                        silencer_gene.distance_to_TSS)
                else:
                    putative_target_genes_table_data_dict[strategy][sub_strategy] = {
                        'gene_name': [silencer_gene.gene_name],
                        'gene_ensembl_id': [silencer_gene.gene_ensembl_id],
                        'genomic_loci': [silencer_gene.genomic_loci],
                        'distance_to_TSS': [silencer_gene.distance_to_TSS],
                    }
            else:
                putative_target_genes_table_data_dict[strategy]['gene_name'].append(silencer_gene.gene_name)
                putative_target_genes_table_data_dict[strategy]['gene_ensembl_id'].append(silencer_gene.gene_ensembl_id)
                putative_target_genes_table_data_dict[strategy]['genomic_loci'].append(silencer_gene.genomic_loci)
                putative_target_genes_table_data_dict[strategy]['distance_to_TSS'].append(silencer_gene.distance_to_TSS)
        else:
            if sub_strategy:
                putative_target_genes_table_data_dict[strategy] = {
                    sub_strategy: {
                        'gene_name': [silencer_gene.gene_name],
                        'gene_ensembl_id': [silencer_gene.gene_ensembl_id],
                        'genomic_loci': [silencer_gene.genomic_loci],
                        'distance_to_TSS': [silencer_gene.distance_to_TSS],
                    }
                }
            else:
                putative_target_genes_table_data_dict[strategy] = {
                    'gene_name': [silencer_gene.gene_name],
                    'gene_ensembl_id': [silencer_gene.gene_ensembl_id],
                    'genomic_loci': [silencer_gene.genomic_loci],
                    'distance_to_TSS': [silencer_gene.distance_to_TSS],
                }
    for strategy,value in putative_target_genes_table_data_dict.items():
        if 'gene_name' in value:
            putative_target_genes_table_data.append(
                {"strategies_algorithm": strategy, "gene_name": ','.join(value['gene_name']),
                 "gene_ensembl_id": ','.join(value['gene_ensembl_id']), "genomic_loci": ','.join(value['genomic_loci']),
                 "distance_to_TSS": ','.join(value['distance_to_TSS'])})
        else:
            putative_target_genes_table_data.append({
                "strategies_algorithm": strategy,
                "gene_name": '<br>'.join([sub_strategy+':'+','.join(gene_info['gene_name']) for sub_strategy, gene_info in value.items()]),
                "gene_ensembl_id": '<br>'.join([sub_strategy+':'+','.join(gene_info['gene_ensembl_id']) for sub_strategy, gene_info in value.items()]),
                "genomic_loci": '<br>'.join([sub_strategy+':'+','.join(gene_info['genomic_loci'])for sub_strategy, gene_info in value.items()]),
                "distance_to_TSS": '<br>'.join([sub_strategy+':'+','.join(gene_info['distance_to_TSS'])for sub_strategy, gene_info in value.items()])
            })
    # 图
    genes_strategies = {}
    for silencer_gene in silencer_genes:
        if genes_strategies.get(silencer_gene.gene_name, None):
            genes_strategies[silencer_gene.gene_name] += '+' + silencer_gene.strategy
        else:
            genes_strategies[silencer_gene.gene_name] = silencer_gene.strategy
    nodes = [{"id": silencer.silencer_id, "name": silencer.silencer_id, "category": 0}]
    nodes += remove_duplicate_dict_list([{
        "id": silencer_gene.gene_name,
        "name": silencer_gene.gene_name,
        "category": list(genes_strategies.keys()).index(silencer_gene.gene_name) + 1
    } for silencer_gene in silencer_genes])
    categories = [{"name": 'silencer'}]
    categories += [{"name": genes_strategy} for genes_strategy in genes_strategies.values()]
    links = remove_duplicate_dict_list(
        [{"source": silencer.silencer_id, "target": silencer_gene.gene_name} for silencer_gene in silencer_genes])
    putative_target_genes_network_data = {"nodes": nodes, "links": links, "categories": categories}
    # Associated Gene Expression
    associated_gene_expressions = []
    for silencer_gene in silencer_genes:
        if any([item.get('gene_name', '') == silencer_gene.gene_name for item in associated_gene_expressions]):
            continue
        gene_expressions = GeneExpression.objects.filter(gene_name=silencer_gene.gene_name)
        source = []
        names = []
        for gene_expression in gene_expressions:
            source.append(gene_expression.expression_value)
            names.append(gene_expression.bio_sample_name)
        if source and names:
            associated_gene_expression = {'gene_name': silencer_gene.gene_name}
            bulk_data = {'source': source, 'names': names}
            associated_gene_expression['bulk_data'] = bulk_data
            associated_gene_expressions.append(associated_gene_expression)

    # Nearby Genomic Features
    


    # Cell / Tissue Type Specificity
    # Linked Silencers In Other Assemblies

    return JsonResponse({
        'signal_in_specific_bio_samples_tables_data': signal_in_specific_bio_samples_tables_data,
        'putative_target_genes': {
            'table_data': putative_target_genes_table_data,
            'network_data': putative_target_genes_network_data,
        },
        'associated_gene_expressions': associated_gene_expressions
    })
