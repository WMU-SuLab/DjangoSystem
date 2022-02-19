# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/12/31 17:18
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
import re

from django.conf import settings
from django.http import HttpResponse


def remove_duplicate_dict_list(dict_list):
    return [dict(t) for t in set([tuple(d.items()) for d in dict_list])]


def ranged_data_response(range_header, relative_path):
    """
    用于根据igv.js的range切分文件，否则文件太大的时候响应会非常慢
    """
    genome_dir_path=settings.GENOME_DIR_PATH
    file_path = os.path.join(genome_dir_path, relative_path)
    if not range_header:
        return None
    match = re.search(r'(\d+)-(\d*)', range_header)
    if not match:
        return "Error: unexpected range header syntax: {}".format(range_header)
    size = os.path.getsize(file_path)
    offset = int(match.group(1))
    length = int(match.group(2) or size) - offset + 1
    with open(file_path, 'rb') as f:
        f.seek(offset)
        data = f.read(length)
    response = HttpResponse(data, status=206, content_type='application/octet-stream')
    response.headers['Content-Range'] = 'bytes {0}-{1}/{2}'.format(offset, offset + length - 1, size)
    return response
