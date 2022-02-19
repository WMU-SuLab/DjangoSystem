# -*- encoding: utf-8 -*-
"""
@File Name      :   gene.py    
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


def generate_gene_unique_name(gene_name, loci):
    return gene_name + '_' + loci


def divide_gene_unique_name(gene_unique_name):
    return gene_unique_name.split('_')


def to_genes_dict(genes):
    return {gene.name: gene for gene in genes}


def filter_genes_any(genes, name):
    for gene in genes:
        if gene.name == name:
            return gene
