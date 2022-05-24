# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/12/7 17:50
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

from django.contrib.auth import views as auth_views
from django.urls import path, include

from SilencerAtlas import app_name
from SilencerAtlas.admin import silencer_atlas_site

# 把urls.py中的urls放到views/__init__.py中
urlpatterns = [
    path('', include(('SilencerAtlas.views.page', app_name), namespace='page')),
    path('api/', include(('SilencerAtlas.views.api', app_name), namespace='api')),
    # silencer atlas 数据库管理
    path('admin/', silencer_atlas_site.urls, name='silencer_atlas_admin'),
    # 增加密码重置功能
    # path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='silencer_atlas_admin_password_reset', ),
    # path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='silencer_atlas_admin_password_reset_done', ),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm', ),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete', ),
]
