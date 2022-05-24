# -*- encoding: utf-8 -*-
"""
@File Name      :   admin.py    
@Create Time    :   2022/3/17 14:29
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
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin

from Common.utils.file_handler.table_handler.xlsx import generate_xlsx_file
from Config.multi_db import MultiDBModelAdmin


class BaseAdminModel(MultiDBModelAdmin):
    # 添加到动作栏
    actions = ['export_data_to_txt', 'export_data_to_excel']

    # 导出数据到txt
    def export_data_to_txt(self, request, queryset):
        # 判断超级用户
        if request.user.is_superuser:
            table_head = list(queryset[0].to_dict().keys())
            table = [[str(item) for item in list(item.to_dict().values())] for item in queryset]
            table.insert(0, table_head)
            with open(os.path.join(settings.BASE_DIR, 'data.txt'), 'a') as f:
                for row in table:
                    f.write('\t'.join(row) + '\r\n')
            # 设置提示信息
            self.message_user(request, '数据导出成功！')
        else:
            # 非超级用户提示警告
            self.message_user(request, '数据导出失败，没有权限！', level=messages.WARNING)

    # 设置函数的显示名称
    export_data_to_txt.short_description = '导出所选数据到txt'

    def export_data_to_excel(self, request, queryset):
        # 判断超级用户
        if request.user.is_superuser:
            table_head = list(queryset[0].to_dict().keys())
            table = [[str(item) for item in list(item.to_dict().values())] for item in queryset]
            table.insert(0, table_head)
            table_sheets = [{'sheet_name': '', 'sheet_data': table}]
            generate_xlsx_file('data.xlsx', table_sheets, settings.BASE_DIR)
            # 设置提示信息
            self.message_user(request, '数据导出成功！')
        else:
            # 非超级用户提示警告
            self.message_user(request, '数据导出失败，没有权限！', level=messages.WARNING)

    export_data_to_excel.short_description = '导出所选数据到excel'


class BaseUserAdminModel(BaseAdminModel, UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # ('Personal info', {'fields': ('is_staff',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
    )
    # 创建用户时显示
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'phone', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'phone')
    ordering = ('username',)
