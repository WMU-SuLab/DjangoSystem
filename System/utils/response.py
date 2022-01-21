# -*- encoding: utf-8 -*-
"""
@File Name      :   response.py    
@Create Time    :   2022/1/7 16:00
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

from django.http.response import JsonResponse as _JsonResponse


class JsonResponse(_JsonResponse):
    data = None
    success = True
    code = 100
    msg = 'success'
    chinese_msg = '成功'

    def __init__(self, data=None, success: bool = True, code: int = 100, msg: str = 'success',
                 chinese_msg: str = '成功', status_code: int = 200, **kwargs):
        self.status_code = status_code
        data = {'data': data, 'success': success, 'status_code': code, 'msg': msg, 'chinese_msg': chinese_msg}
        super().__init__(data, **kwargs)
