# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py    
@Create Time    :   2022/3/18 15:55
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

from django.conf import settings

APP_DIR = os.path.join(settings.BASE_DIR, 'Common')
app_name = 'Common'
database_name = 'Common'
