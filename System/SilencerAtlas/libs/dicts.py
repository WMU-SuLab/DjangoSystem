# -*- encoding: utf-8 -*-
"""
@File Name      :   genome_file.py    
@Create Time    :   2022/2/28 17:06
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

from Common.utils.text_handler.dicts import dict_to_tree, get_tree_ids

genome_data = {
    'human': {
        'heart': ['ENCSR000APE.subtract.sort.bw'],
    },
    'mouse': {
        'brain': ['ENCSR000EWB.subtract.sort.bw'],
    }
}

genome_tree_data = dict_to_tree(genome_data)
genome_files_data = get_tree_ids(genome_tree_data)
