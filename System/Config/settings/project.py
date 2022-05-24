# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py    
@Create Time    :   2022/4/19 17:34
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

from .base import *

# 以下是自己定义的项目中需要用到的配置
# genome文件位置
GENOME_DIR_PATH = os.path.join(BASE_DIR, 'SilencerAtlas', 'libs', 'genome')
# 数据库限制一次最多查询数量
MODEL_TOTAL_LIMIT = 1000
