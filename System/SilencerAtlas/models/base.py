# -*- encoding: utf-8 -*-
"""
@File Name      :   base.py    
@Create Time    :   2021/12/7 20:01
@Description    :   
@Version        :   
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

from hashid_field import BigHashidAutoField

from Common.models.base import BaseModel


class Base(BaseModel):
    id = BigHashidAutoField(
        primary_key=True,
        # 允许使用加密过的id查询
        allow_int_lookup=True,
        # 不返回对象而是直接返回加密后的字符串
        enable_hashid_object=False
    )

    class Meta:
        abstract = True
        app_label = 'SilencerAtlas'
