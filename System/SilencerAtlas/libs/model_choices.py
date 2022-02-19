# -*- encoding: utf-8 -*-
"""
@File Name      :   model_items.py    
@Create Time    :   2021/12/29 20:39
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
# 主要用于页面的快速展示
unknown = {
    '':'',
    'unknown': 'unknown',
    '-':'-',
    '--':'--',
}
sources = {
    'encode': 'ENCODE',
    'roadmap': 'Roadmap',
    'geo': 'GEO'
}
species = {
    'human': 'Human',
    'mouse': 'Mouse'
}
bio_sample_types = {
    'tissue': 'Tissue',
    'cellline': 'Cell Line',
    'primary_cell': 'Primary Cell',
    'diff_cell': 'In vitro differentiated cells',
}
recognition_factors = {
    'h3k9me1': 'H3K9me1',
    'h3k9me2': 'H3K9me2',
    'h3k9me3': 'H3K9me3',
    'h3k27me3': 'H3K27me3',
    'h3k79me3': 'H3K79me3',
    'h4k20me1': 'H4K20me1',
}
strategies = {
    # 'closest': 'Closest',
    # 'overlap': 'Overlap',
    # 'abc_model': 'ABC Model'
    'spacial_overlap':'Spatial Overlap',
    'physical_nearest':'Physical Nearest',
    'homer_nearest':'HOMER Nearest',
}
variants = {
    'eQTL': 'eQTL',
    'risk_snp': 'Risk SNP'
}
strand = {
    # 正链
    # '+': 'positive',
    '+': '+',
    # 负链
    # '-': 'negative',
    '-': '-',
    # 不需要指定
    # '.': 'needless',
    '.': '.',
}
