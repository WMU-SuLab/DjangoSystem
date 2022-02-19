# -*- encoding: utf-8 -*-
"""
@File Name      :   snp.py    
@Create Time    :   2022/1/23 21:44
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

def to_snps_dict(snps):
    return {snp.rs_id: snp for snp in snps}

def filter_snps_any(snps, rs_id):
    for snp in snps:
        if snp.rs_id == rs_id:
            return rs_id
