# -*- encoding: utf-8 -*-
"""
@File Name      :   command.py    
@Create Time    :   2022/2/21 9:59
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

from abc import ABCMeta

from django.core.management.base import BaseCommand as DjangoBaseCommand


class BaseCommand(DjangoBaseCommand, metaclass=ABCMeta):
    def add_arguments(self, parser):
        parser.add_argument('-f','--file_path', type=str, help='data file path')
        parser.add_argument('--dir_path', type=str, help='data directory path')
        parser.add_argument('--chunk_size', type=int, default=0, help='chunk size')
        parser.add_argument('--skip_rows', type=int, default=0, help='skip rows')
