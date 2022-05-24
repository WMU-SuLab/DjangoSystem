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
import random
from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST
from django.urls import reverse
from SilencerAtlas.utils import ranged_data_response
from SilencerAtlas.libs.dicts import genome_files_data
from SilencerAtlas.libs.lists import igv_colors


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


@require_POST
def get_igv_tracks(request):
    """
    暂时是bw文件，后续可以集成其他格式
    """
    get_igv_file_data_url=reverse('SilencerAtlas:api:data:v1_0:get_igv_file_data',args=['test_file_path']).replace('test_file_path','')
    file_url_prefix= get_igv_file_data_url+ "self/bw/"
    data=request.json
    # print(data)
    checked_keys=data.get('checkedKeys',[])
    tracks= []
    for checked_key in checked_keys:
        genome_files= genome_files_data.get(checked_key,[])
        for file in genome_files:
            name=file.split('.')[0]
            tracks.append({
                "name": name,
                "url": file_url_prefix+file,
                "type": "wig",
                "format": "bigwig",
                "sourceType": "file",
                "min": "0.1",
                "max": "0.3",
                "color": random.choice(igv_colors),
                'guideLines': [
                    {'color': 'green', 'dotted': True, 'y': 25},
                    {'color': 'red', 'dotted': False, 'y': 5}
                ]
            })


    # tracks = [
    #     {
    #         "name": "ENCSR024JJL",
    #         "url": get_igv_file_data_url+"self/bw/ENCSR024JJL.subtract.bw",
    #         "type": "wig",
    #         "format": "bigwig",
    #         "sourceType": "file",
    #         "min": "0",
    #         # "max": "0.1",
    #         "max": "0.3",
    #         # "color": "#1890ff",
    #         "color":'#fff566',
    #     },
    #     {
    #         "name": "ENCSR049FUB",
    #         "url": get_igv_file_data_url+"self/bw/ENCSR049FUB.subtract.bw",
    #         "type": "wig",
    #         "format": "bigwig",
    #         "sourceType": "file",
    #         "min": "0",
    #         # "max": "0.1",
    #         "max": "0.3",
    #         # "color": "#1890ff",
    #         "color":"#389e0d",
    #     },
    #     {
    #         "name": "ENCSR057BFO",
    #         "url": get_igv_file_data_url+"self/bw/ENCSR057BFO.subtract.bw",
    #         "type": "wig",
    #         "format": "bigwig",
    #         "sourceType": "file",
    #         "min": "0",
    #         # "max": "0.1",
    #         "max": "0.3",
    #         # "color": "#1890ff",
    #         "color":"#08979c"
    #     },
    #     {
    #         "name": "ENCSR177CGN",
    #         "url": get_igv_file_data_url+"self/bw/ENCSR177CGN.subtract.bw",
    #         "type": "wig",
    #         "format": "bigwig",
    #         "sourceType": "file",
    #         "min": "0",
    #         # "max": "0.2",
    #         "max": "0.3",
    #         # "color": "#ff4d4f",
    #         "color":"#722ed1"
    #     },
    #     {
    #         "name": "ENCSR188HXK",
    #         "url": get_igv_file_data_url+"self/bw/ENCSR188HXK.subtract.bw",
    #         "type": "wig",
    #         "format": "bigwig",
    #         "sourceType": "file",
    #         "min": "0",
    #         # "max": "1",
    #         "max": "0.2",
    #         # "color": "#ff4d4f",
    #         "color":"#ff441a"
    #     },
    #     {
    #         "name": "ENCSR200AFX",
    #         "url": get_igv_file_data_url+"self/bw/ENCSR200AFX.subtract.bw",
    #         "type": "wig",
    #         "format": "bigwig",
    #         "sourceType": "file",
    #         "min": "0",
    #         # "max": "0.1",
    #         "max": "0.3",
    #         # "color": "#ff4d4f",
    #         "color":"#a3b61f"
    #     },
    #     {
    #         "name": "ENCSR543UBL",
    #         "url": get_igv_file_data_url+"self/bw/ENCSR543UBL.subtract.bw",
    #         "type": "wig",
    #         "format": "bigwig",
    #         "sourceType": "file",
    #         "min": "0",
    #         # "max": "0.5",
    #         "max": "0.3",
    #         # "color": "#ff4d4f",
    #         "color":"#75856d"
    #     },
    #     {
    #         "name": "ENCSR952BJX",
    #         "url": get_igv_file_data_url + "self/bw/ENCSR952BJX.subtract.bw",
    #         "type": "wig",
    #         "format": "bigwig",
    #         "sourceType": "file",
    #         "min": "0",
    #         # "max": "1",
    #         "max": "0.3",
    #         # "color": "#1890ff",
    #         "color":"#c78738"
    #     },
    #     {
    #         "name": "ENCSR067VEM",
    #         "url": get_igv_file_data_url + "self/bw/ENCSR067VEM.subtract.sort.bw",
    #         "type": "wig",
    #         "format": "bigwig",
    #         "sourceType": "file",
    #         "min": "0",
    #         # "max": "0.5",
    #         "max": "0.6",
    #         # "color": "#ff4d4f",
    #         "color":"#cc0000"
    #     },
    #     {
    #         "name": "ENCSR000APE",
    #         "url": get_igv_file_data_url + "self/bw/ENCSR000APE.subtract.sort.bw",
    #         "type": "wig",
    #         "format": "bigwig",
    #         "sourceType": "file",
    #         "min": "0",
    #         # "max": "0.5",
    #         "max": "0.6",
    #         # "color": "#ff4d4f",
    #         "color": "#cc0000"
    #     },
    #     {
    #         "name": "ENCSR000EWB",
    #         "url": get_igv_file_data_url + "self/bw/ENCSR000EWB.subtract.sort.bw",
    #         "type": "wig",
    #         "format": "bigwig",
    #         "sourceType": "file",
    #         "min": "0",
    #         # "max": "0.5",
    #         "max": "0.6",
    #         # "color": "#ff4d4f",
    #         "color": "#cc0000"
    #     },
    #     {
    #         "name": "ENCSR404LJZ",
    #         "url": get_igv_file_data_url + "self/bw/ENCSR404LJZ.subtract.sort.bw",
    #         "type": "wig",
    #         "format": "bigwig",
    #         "sourceType": "file",
    #         "min": "0",
    #         # "max": "0.5",
    #         "max": "0.6",
    #         # "color": "#ff4d4f",
    #         "color": "#cc0000"
    #     }
    # ]
    return JsonResponse({'tracks': tracks})


def get_igv_file_data(request, relative_path):
    range_header = request.headers.get('Range', None)
    return ranged_data_response(range_header=range_header, relative_path=relative_path)
