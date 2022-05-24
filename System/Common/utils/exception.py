
# -*- encoding: utf-8 -*-
"""
@File Name      :   exception.py    
@Create Time    :   2022/4/2 14:23
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

from rest_framework.views import exception_handler as _exception_handler
from rest_framework.views import Response
from rest_framework import status


# 将仅针对由引发的异常生成的响应调用异常处理程序，它不会用于视图直接返回的任何响应
def exception_handler(exc, context):
    response = _exception_handler(exc, context)

    # 这个循环是取第一个错误的提示用于渲染
    for index, value in enumerate(response.data):
        if index == 0:
            key = value
            value = response.data[key]
            if isinstance(value, str):
                message = value
            else:
                message = key + value[0]
    if response is None:
        # 错误原因
        # print(exc)
        # 错误信息
        # print(context)
        # print('%s - %s - %s' % (context['view'], context['request'].method, exc))
        return Response({
            'msg': '服务器错误'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)
    else:
        # print('%s - %s - %s' % (context['view'], context['request'].method, exc))
        return Response({
            'msg': message,
        }, status=response.status_code, exception=True)