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

from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import BigHashidAutoField


class StatusChoices(models.IntegerChoices):
    # 如果没有提供元组，或者最后一项不是（惰性）字符串，label是从成员名自动生成。
    STATUS_NORMAL = 1, _('正常')
    STATUS_DELETE = 0, _('删除')
    STATUS_TRASH = -1, _('回收站中删除')


class Base(models.Model):
    # 默认设置了主键id，所以基本除了外键不需要进行配置primary key
    # 所有字段默认不允许为空
    # 配置了unique的字段不需要再配置db_index索引
    # 可以通过db_column字段指定列名

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_TRASH = -1
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_TRASH, '回收站中删除')
    )
    id = BigHashidAutoField(
        primary_key=True,
        # 允许使用加密过的id查询
        allow_int_lookup=True,
        # 不返回对象而是直接返回加密后的字符串
        enable_hashid_object=False
    )
    # 注意：auto_now、auto_now_add和default三个会互相排斥
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')
    # choice要显示完整的内容，需要调用Model.get_FOO_display()
    # 参考https://docs.djangoproject.com/zh-hans/3.2/ref/models/instances/#django.db.models.Model.get_FOO_display
    # 即使不在choices中也是可以成功的，只是get_FOO_display()显示的还是自身值
    status = models.IntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    remarks = models.CharField(max_length=1000, default='', blank=True, verbose_name='备注')
    remarks_json = models.JSONField(default=dict, blank=True, verbose_name='json类型的额外信息')

    # Meta用于配置Model的一些属性
    # 更多模型可选参数详见：https://docs.djangoproject.com/zh-hans/3.2/ref/models/options/
    class Meta:
        # db_table:数据库表名
        # ordering：这是一个字符串和／或查询表达式的元组或列表。每一个字符串都是一个字段名，前面有一个可选的“-”字头，表示降序。没有前缀“-”的字段将按升序排列。使用字符串“?”来随机排序。
        # verbose_name和verbose_name_plural：阅读友好的单复数名
        # abstract：是否是抽象类，设置为抽象类在数据库中不会构建
        # Django在安装Meta属性前，对抽象基类的Meta做了一个调整——设置abstract = False。这意味着抽象基类的子类不会自动地变成抽象类。
        # 为了继承一个抽象基类创建另一个抽象基类，你需要在子类上显式地设置abstract = True。
        abstract = True
        # 必须要指定表的 app_label 名字，如果不指定则会创建到 default 中配置的数据库名下
        # 注意是app_name，不是database_name
        app_label = 'SilencerAtlas'

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    def to_dict(self, fields=None, exclude=None):
        data = {}
        for field in self._meta.concrete_fields + self._meta.many_to_many:
            value = field.value_from_object(self)
            if fields and field.name not in fields:
                continue
            if exclude and field.name in exclude:
                continue
            if isinstance(field, models.ManyToManyField):
                value = [i.id for i in value] if self.pk else None
            if isinstance(field, models.DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None
            data[field.name] = value
        return data
