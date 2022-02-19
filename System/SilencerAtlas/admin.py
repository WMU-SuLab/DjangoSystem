import os

from django.conf import settings
from django.contrib import admin, messages

from ManageSys.multi_db import MultiDBModelAdmin
from SilencerAtlas.models.gene import Gene, GeneExpression
from SilencerAtlas.models.recognition_factor import RecognitionFactor
from SilencerAtlas.models.region import Region
from SilencerAtlas.models.sample import Sample
from SilencerAtlas.models.silencer import Silencer, SilencerGenes, SilencerTFBs, SilencerCas9s, SilencerSNPs, \
    SilencerRecognitionFactors, SilencerSampleRecognitionFactors
from SilencerAtlas.models.snp import SNP
from utils.file_handler.table_handler.xlsx import generate_xlsx_file

# 注意使用AdminSite创建的site注册之后不能使用装饰器的写法，只能使用函数写法
# 如果仍然需要使用装饰器的写法，使用admin.register(...,site=)的写法
silencer_atlas_site = admin.AdminSite('silencer_atlas')
silencer_atlas_site.site_title = 'Silencer Atlas数据库后台管理'
silencer_atlas_site.site_header = 'Silencer Atlas'


# Register your models here.
class BaseAdmin(MultiDBModelAdmin):
    # 设置连接的数据库
    using = 'SilencerAtlas'
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


class RegionAdmin(BaseAdmin):
    list_display = ('id', 'chr', 'start', 'end')
    list_filter = ('status', 'created_time',)
    search_fields = ['chr', 'start', 'end']
    fieldsets = (
        (None, {
            'fields': (
                ('chr', 'start', 'end',),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(Region, RegionAdmin)


# 注意，内联是在父模型（外键指定的模型）中编辑子模型
class RegionInline(admin.TabularInline):
    model = Region
    extra = 0
    fields = ('chr', 'start', 'end')


class GeneAdmin(BaseAdmin):
    list_display = ('id', 'name', 'ensembl_id', 'region', 'strand', 'bio_type')
    list_filter = ('status', 'created_time', 'strand', 'bio_type')
    search_fields = ['name', 'ensembl_id', 'bio_type', 'region', 'strand']
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'ensembl_id', 'bio_type'),
                ('region', 'strand',),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(Gene, GeneAdmin)


# class GeneExpressionAdmin(BaseAdmin):
#     list_display = ('id', 'gene', 'bio_sample_name', 'expression_value')
#     list_filter = ('status', 'created_time',)
#     search_fields = ['gene', 'bio_sample_name', 'expression_value']
#     fieldsets = (
#         (None, {
#             'fields': (
#                 ('gene', 'bio_sample_name', 'expression_value',),
#                 ('remarks', 'remarks_json', 'status'),
#             )
#         }),
#     )


# silencer_atlas_site.register(GeneExpression, GeneExpressionAdmin)


class SNPAdmin(BaseAdmin):
    list_display = ('id', 'rs_id', 'region',)
    list_filter = ('status', 'created_time')
    search_fields = ['rs_id']
    fieldsets = (
        (None, {
            'fields': (
                ('rs_id',),
                ('region',),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(SNP, SNPAdmin)


class RecognitionFactorAdmin(BaseAdmin):
    list_display = ('id', 'name')
    list_filter = ('status', 'created_time', 'name')
    search_fields = ['name']
    fieldsets = (
        (None, {
            'fields': (
                ('name',),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(RecognitionFactor, RecognitionFactorAdmin)


class SampleAdmin(BaseAdmin):
    list_display = ('id', 'sample_id', 'bio_sample_name', 'tissue_type', 'bio_sample_type', 'species', 'source')
    list_filter = ('status', 'created_time', 'tissue_type', 'bio_sample_type', 'species', 'source')
    search_fields = ['sample_id', 'bio_sample_name', 'tissue_type', 'bio_sample_type', 'species', 'source']
    fieldsets = (
        (None, {
            'fields': (
                ('sample_id', 'bio_sample_name',),
                ('tissue_type', 'bio_sample_type', 'species', 'source'),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(Sample, SampleAdmin)


class SilencerAdmin(BaseAdmin):
    # 设置list_display来控制哪些字段显示在变更页面的表格中
    list_display = (
        'id', 'silencer_id', 'region', 'score', 'strand',
    )
    # 设置list_filter来激活管理更改列表页面右侧侧栏的过滤器
    list_filter = ('status', 'created_time',)
    # 设置search_fields，在管理更改列表页面上启用搜索框
    search_fields = ['silencer_id', 'region', 'score', 'strand', ]

    # 通过fields和exclude字段指定在表“添加”和“更改”页面单中显示和排除哪些字段

    # 设置fieldsets来控制管理员“添加”和“更改”页面的布局
    fieldsets = (
        (None, {
            'fields': (
                ('silencer_id',),
                ('region',),
                ('score', 'strand',),
                ('sample',),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(Silencer, SilencerAdmin)


class SilencerGenesAdmin(BaseAdmin):
    list_display = ('silencer', 'gene_name', 'gene_ensembl_id','genomic_loci','strategy','sub_strategy','distance_to_TSS')
    list_filter = ('status', 'created_time', 'strategy')
    search_fields = ['silencer', 'gene_name', 'gene_ensembl_id','genomic_loci','strategy','sub_strategy','distance_to_TSS']
    fieldsets = (
        (None, {
            'fields': (
                ('silencer', 'gene_name', 'gene_ensembl_id','genomic_loci',),
                ('strategy','sub_strategy','distance_to_TSS',),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(SilencerGenes, SilencerGenesAdmin)


class SilencerTFBsAdmin(BaseAdmin):
    list_display = ('silencer', 'transcription_factor', 'binding_site')
    list_filter = ('status', 'created_time')
    search_fields = ['silencer', 'transcription_factor', 'binding_site']
    fieldsets = (
        (None, {
            'fields': (
                ('silencer', 'transcription_factor', 'binding_site'),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(SilencerTFBs, SilencerTFBsAdmin)


class SilencerSNPsAdmin(BaseAdmin):
    list_display = ('silencer', 'snp', 'variant')
    list_filter = ('status', 'created_time', 'variant')
    search_fields = ['silencer', 'snp', 'variant']
    fieldsets = (
        (None, {
            'fields': (
                ('silencer', 'snp'),
                ('variant',),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(SilencerSNPs, SilencerSNPsAdmin)


class SilencerCas9sAdmin(BaseAdmin):
    list_display = ('silencer', 'region')
    list_filter = ('status', 'created_time')
    search_fields = ['silencer', 'region']
    fieldsets = (
        (None, {
            'fields': (
                ('silencer', 'region'),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(SilencerCas9s, SilencerCas9sAdmin)


class SilencerRecognitionFactorsAdmin(BaseAdmin):
    list_display = ('silencer', 'recognition_factor',)
    list_filter = ('status', 'created_time', 'recognition_factor')
    search_fields = ['silencer', 'recognition_factor', ]
    fieldsets = (
        (None, {
            'fields': (
                ('silencer', 'recognition_factor'),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(SilencerRecognitionFactors, SilencerRecognitionFactorsAdmin)


class SilencerSampleRecognitionFactorsAdmin(BaseAdmin):
    list_display = ('silencer', 'recognition_factor', 'bio_sample_name', 'z_score', 'recognized')
    list_filter = ('status', 'created_time', 'recognition_factor', 'bio_sample_name',)
    search_fields = ['silencer', 'recognition_factor', 'bio_sample_name', 'z_score', 'recognized']
    fieldsets = (
        (None, {
            'fields': (
                ('silencer', 'recognition_factor','bio_sample_name',),
                ( 'z_score', 'recognized',),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(SilencerSampleRecognitionFactors, SilencerSampleRecognitionFactorsAdmin)
