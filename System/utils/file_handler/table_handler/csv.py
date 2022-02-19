# -*- encoding: utf-8 -*-
"""
@File Name      :   csv.py    
@Create Time    :   2022/2/19 15:28
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

import pandas as pd


def read_csv_n_lines_each_time_by_pandas_yield(file_path,sep='\t', chunk_size=1000,  skip_rows: int = 0):
    count = 0
    for df in pd.read_csv(file_path, sep=sep, chunksize=chunk_size, skiprows=skip_rows):
        count += 1
        print(f'reading {(count - 1) * chunk_size + 1 + skip_rows}-{count * chunk_size + skip_rows} rows')
        yield df
