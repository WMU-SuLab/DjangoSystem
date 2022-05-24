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

from rest_framework.renderers import JSONRenderer as _JSONRenderer

# 重写drf的JSONRenderer
class JSONRenderer(_JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            # 判断实例的类型，返回的数据可能是列表也可能是字典
            if isinstance(data, dict):
                # 如果是字典的话应该是返回的数据，会包含msg,code,status等字段必须抽离出来
                msg = data.pop('msg', 'success')
                chinese_msg = data.pop('chinese_msg', '成功')
                code = data.pop('code', 100)
                success = data.pop('success', 'unknown')
                if success =='unknown':
                    success = True if code <= 100 else False
                status_code = data.pop('status_code', 200)
            else:
                msg = 'success'
                chinese_msg = '成功'
                code = 100
                success = True
                status_code = 200
            # 自定义返回数据格式
            ret = {
                'code': code,
                'success': success,
                'status_code': status_code,
                'msg': msg,
                'chinese_msg': chinese_msg,
                'test':True,
                'data': data,
            }
            # 返回JSON数据
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)


# 重写django原生的JsonResponse
class JsonResponse(_JsonResponse):
    data = None
    success = True
    code = 100
    msg = 'success'
    chinese_msg = '成功'

    def __init__(
            self, data=None, success: bool = True, code: int = 100, status_code: int = 200,
            msg: str = 'success', chinese_msg: str = '成功', **kwargs):
        self.status_code = status_code
        data = {'data': data, 'success': success, 'status_code': code, 'msg': msg, 'chinese_msg': chinese_msg}
        super().__init__(data, **kwargs)
