# -*- encoding: utf-8 -*-
"""
@File Name      :   silencer.py    
@Create Time    :   2022/1/19 14:28
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
from django.views.decorators.http import require_POST, require_GET
from SilencerAtlas.models.silencer import Silencer
from utils.response import JsonResponse

@require_GET
def get_silencer(request, silencer_id):
    """
    单个查询silencer
    :param request:
    :param silencer_id:
    :return:
    """
    silencer = Silencer.objects.prefetch_related('region', 'sample').filter(silencer_id=silencer_id).first()
    if silencer:
        return JsonResponse({
            'silencer': {
                'silencer_id': silencer.silencer_id,
                'chromosome': silencer.region.chromosome,
                'start': silencer.region.start,
                'end': silencer.region.end,
                'strand': silencer.strand,
                'score': silencer.score,
            },
            'sample': {
                'bio_sample_name': silencer.sample.bio_sample_name,
                'tissue_cell_type': silencer.sample.tissue_type,
                'bio_sample_type': silencer.sample.bio_sample_type,
                'species': silencer.sample.species,
                'source': silencer.sample.source,
            },
            'target_genes': [{
                'gene_name': silencer_gene.gene.name,
                'strategy': silencer_gene.stratrgy,
                # 'sample_expression': [{
                #     'bio_sample_name': gene_expression.bio_sample_name,
                #     'expression_value': gene_expression.expression_value
                # } for gene_expression in silencer_gene.gene.expressions.all()],
            } for silencer_gene in silencer.silencergenes_set.all()],
            'TFBs': [{
                silencer_tfb.transcription_factor:
                    silencer_tfb.binding_site.loci} for silencer_tfb in silencer.silencertfbs_set.all()
            ],
            'SNPs': [{
                'rs_id': silencer_snp.snp.rs_id,
                'variant': silencer_snp.variant,
            } for silencer_snp in silencer.silencersnps_set.all()]
        })
    else:
        return JsonResponse(data={}, success=False, code=999, msg='no this silencer', chinese_msg='没有这个silencer')

@require_POST
def get_silencers(request):
    """
    批量查询silencer
    :param request:
    :return:
    """
    data=request.json
    return JsonResponse({})