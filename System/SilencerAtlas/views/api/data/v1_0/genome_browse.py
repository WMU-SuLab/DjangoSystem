# -*- encoding: utf-8 -*-
"""
@File Name      :   genome_browse.py    
@Create Time    :   2021/12/28 19:43
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

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.urls import reverse,reverse_lazy
from SilencerAtlas.utils import ranged_data_response


@require_GET
def get_igv_reference(request):
    reference = {
        "id": "hg38",
        "name": "Human (GRCh38/hg38)",
        "fastaURL": "https://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa",
        "indexURL": "https://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa.fai",
        "cytobandURL": "https://s3.amazonaws.com/igv.org.genomes/hg38/annotations/cytoBandIdeo.txt.gz",
        "aliasURL": "https://s3.amazonaws.com/igv.org.genomes/hg38/hg38_alias.tab",
        # "tracks": [
        #     {
        #         "name": "Refseq Genes",
        #         "format": "refgene",
        #         "url": "https://s3.amazonaws.com/igv.org.genomes/hg38/ncbiRefSeq.sorted.txt.gz",
        #         "indexURL": "https://s3.amazonaws.com/igv.org.genomes/hg38/ncbiRefSeq.sorted.txt.gz.tbi",
        #         "visibilityWindow": -1,
        #         "removable": False,
        #         "order": 1000000,
        #         "infoURL": "https://www.ncbi.nlm.nih.gov/gene/?term=$$"
        #     }
        # ],
        "chromosomeOrder": "chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, " +
                           "chr11, chr12, chr13, chr14, chr15, chr16, chr17, chr18, chr19, " +
                           "chr20, chr21, chr22, chrX, chrY"
    }
    return JsonResponse({'reference': reference})


@require_GET
def get_igv_tracks(request):
    """
    暂时是bw文件，后续可以集成其他格式
    """
    # files = os.listdir(file_dir)
    # tracks = [{
    #     "name": file.split('.')[0],
    #     "url": "/get_igv_file_data/bw/" + file,
    #     "type": "wig",
    #     "format": "bigwig",
    #     "sourceType": "file",
    #     "min": "0",
    #     "max": "0.1",
    #     "color": "rgb(0, 0, 150)",
    #     "guideLines": [
    #         {"color": 'green', "dotted": True, "y": 25},
    #         {"color": 'red', "dotted": False, "y": 5}
    #     ]
    # } for file in files]
    get_igv_file_data_url=reverse('SilencerAtlas:api:data:v1_0:get_igv_file_data',args=['test_file_path']).replace('test_file_path','')
    tracks = [
        {
            "name": "ENCSR952BJX",
            "url": get_igv_file_data_url+"self/bw/ENCSR952BJX.subtract.bw",
            "type": "wig",
            "format": "bigwig",
            "sourceType": "file",
            "min": "0",
            "max": "1",
            "color": "#1890ff",
        },
        {
            "name": "ENCSR024JJL",
            "url": get_igv_file_data_url+"self/bw/ENCSR024JJL.subtract.bw",
            "type": "wig",
            "format": "bigwig",
            "sourceType": "file",
            "min": "0",
            "max": "0.1",
            "color": "#1890ff",
        },
        {
            "name": "ENCSR049FUB",
            "url": get_igv_file_data_url+"self/bw/ENCSR049FUB.subtract.bw",
            "type": "wig",
            "format": "bigwig",
            "sourceType": "file",
            "min": "0",
            "max": "0.1",
            "color": "#1890ff",
        },
        {
            "name": "ENCSR057BFO",
            "url": get_igv_file_data_url+"self/bw/ENCSR057BFO.subtract.bw",
            "type": "wig",
            "format": "bigwig",
            "sourceType": "file",
            "min": "0",
            "max": "0.1",
            "color": "#1890ff",
        },
        {
            "name": "ENCSR177CGN",
            "url": get_igv_file_data_url+"self/bw/ENCSR177CGN.subtract.bw",
            "type": "wig",
            "format": "bigwig",
            "sourceType": "file",
            "min": "0",
            "max": "0.2",
            "color": "#ff4d4f",
        },
        {
            "name": "ENCSR188HXK",
            "url": get_igv_file_data_url+"self/bw/ENCSR188HXK.subtract.bw",
            "type": "wig",
            "format": "bigwig",
            "sourceType": "file",
            "min": "0",
            "max": "1",
            "color": "#ff4d4f",
        },
        {
            "name": "ENCSR200AFX",
            "url": get_igv_file_data_url+"self/bw/ENCSR200AFX.subtract.bw",
            "type": "wig",
            "format": "bigwig",
            "sourceType": "file",
            "min": "0",
            "max": "0.1",
            "color": "#ff4d4f",
        },
        {
            "name": "ENCSR543UBL",
            "url": get_igv_file_data_url+"self/bw/ENCSR543UBL.subtract.bw",
            "type": "wig",
            "format": "bigwig",
            "sourceType": "file",
            "min": "0",
            "max": "0.5",
            "color": "#ff4d4f",
        },
    ]
    return JsonResponse({'tracks': tracks})


def get_igv_file_data(request, relative_path):
    range_header = request.headers.get('Range', None)
    return ranged_data_response(range_header=range_header, relative_path=relative_path)
