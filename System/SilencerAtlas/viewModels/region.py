# -*- encoding: utf-8 -*-
"""
@File Name      :   region.py    
@Create Time    :   2021/12/31 17:14
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


def filter_regions_any(regions, chromosome, start, end):
    for region in regions:
        if region.chromosome == chromosome and region.start == start and region.end == end:
            return region


def divide_region(region: str):
    """
    :param region: str类型，通用的格式为chr:start-end
    :return: chromosome, start, end
    """
    chromosome, locus = region.split(':')
    start, end = locus.split('-')
    return chromosome.lower(), start, end


def generate_region(chromosome, start, end):
    return f'{chromosome}:{start}-{end}'


def to_regions_dict(regions):
    return {generate_region(region.chromosome, region.start, region.end): region for region in regions}
