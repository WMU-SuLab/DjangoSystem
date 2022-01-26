# -*- encoding: utf-8 -*-
"""
@File Name      :   test.py    
@Create Time    :   2021/12/29 14:47
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

# 测试完成后请删除所有代码
import time

# import pandas as pd

start = time.perf_counter()

# count = 0
# with open('D:\Coding\Python\Django-backend\System\SilencerAtlas\libs\esophagus_muscularis_mucosa.integrate.txt',
#           'r') as f, \
#         open('D:\Coding\Python\Django-backend\System\SilencerAtlas\libs\\1.txt', 'w') as w:
#     head = f.readline()
#     rows = f.readlines()
#     header = ['silencer_id', 'silencer_name', 'chr', 'start', 'end', 'score', 'strand', 'bio_sample_name', 'tissue_cell_type',
#               'bio_sample_type','species','source','target_genes','recognition_factors','samples_recognition_factors_z_score']
#     new_rows = ['\t'.join(header) + '\n']
#     for row in rows:
#         cols = row.strip().split('\t')
#         new_cols = [
#             cols[3],
#             cols[5],
#             cols[0], cols[1], cols[2],
#             cols[4], '+', cols[10], cols[9], cols[8], cols[6], 'encode',
#             cols[15] + ':overlap;' + cols[16] + ':closest', cols[12],
#             'esophagus_muscularis_mucosa-h3k27me3-1:' + cols[13] +
#             ';esophagus_squamous_epithelium-h3k27me3-1:' + cols[14], ]
#         new_rows.append('\t'.join(new_cols) + '\n')
#     w.writelines(new_rows)
# genes=pd.read_csv('D:\Coding\Python\Django-backend\System\SilencerAtlas\libs\Homo_sapiens.GRCh38.95.gene.bed',sep='\t',names=['chr','start','end','strand','enm','name','type'])['name'].tolist()
# print(len(genes))
# genes2=[]
# for df in pd.read_csv('D:\Coding\Python\Django-backend\System\SilencerAtlas\libs/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct',sep='\t',chunksize=10000,skiprows=2):
#     genes2+=df['Description'].tolist()
# gene1_2=set(genes)-set(genes2)
# gene2_1=set(genes2)-set(genes)
# with open('D:\Coding\Python\Django-backend\System\SilencerAtlas\libs/gene_use_have.txt','w') as w:
#     w.write(str(len(gene1_2))+'\n')
#     w.writelines([row+'\n' for row in list(gene1_2)])
# with open('D:\Coding\Python\Django-backend\System\SilencerAtlas\libs/gene_have_use.txt','w') as w:
#     w.write(str(len(gene2_1))+'\n')
#     w.writelines([row+'\n' for row in list(gene2_1)])

# with open('D:\Coding\Python\Django-backend\System\SilencerAtlas\libs/1.txt', 'r') as f1, open(
#         'D:\Coding\Python\Django-backend\System\SilencerAtlas\libs/2.txt', 'r') as f2, open(
#         'D:\Coding\Python\Django-backend\System\SilencerAtlas\libs/all.txt', 'w') as w:
#     w.write(f1.readline())
#     f2.readline()
#     w.writelines(f1.readlines())
#     w.writelines(f2.readlines())


print(f'{time.perf_counter() - start}')
