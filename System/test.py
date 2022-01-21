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
start = time.perf_counter()

# count = 0
# with open('D:\Coding\Python\Django-backend\System\SilencerAtlas\libs\esophagus_squamous_epithelium.integrate.txt',
#           'r') as f, \
#         open('D:\Coding\Python\Django-backend\System\SilencerAtlas\libs\\2.txt', 'w') as w:
#     head = f.readline()
#     rows = f.readlines()
#     header = ['silencer_id', 'silencer_name', 'chr', 'start', 'end', 'score', 'strand', 'bio_sample_name', '',
#               'bio_sample_type']
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
print(f'{time.perf_counter() - start}')
