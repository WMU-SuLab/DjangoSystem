from django.contrib import admin

from SilencerAtlas.models.gene import Gene, GeneRegion, GeneExpression
from SilencerAtlas.models.recognition_factor import RecognitionFactor
from SilencerAtlas.models.region import CommonRegion
from SilencerAtlas.models.sample import Sample
from SilencerAtlas.models.silencer import Silencer, SilencerGene, SilencerTranscriptionFactor, SilencerCas9, \
    SilencerSNP, \
    SilencerRecognitionFactor, SilencerSampleRecognitionFactor
from SilencerAtlas.models.snp import SNP
from Common.models.admin import BaseAdminModel

# 注意使用AdminSite创建的site注册之后不能使用装饰器的写法，只能使用函数写法
# 如果仍然需要使用装饰器的写法，使用admin.register(...,site=)的写法
silencer_atlas_site = admin.AdminSite('silencer_atlas')
silencer_atlas_site.site_title = 'Silencer Atlas数据库后台管理'
silencer_atlas_site.site_header = 'Silencer Atlas'


# Register your models here.
class BaseAdmin(BaseAdminModel):
    # 设置连接的数据库
    using = 'SilencerAtlas'


class CommonRegionAdmin(BaseAdmin):
    list_display = ['id', 'chr', 'start', 'end']
    list_filter = ['status', 'created_time', ]
    search_fields = ['chr', 'start', 'end']
    fieldsets = (
        (None, {
            'fields': (
                ('chr', 'start', 'end',),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(CommonRegion, CommonRegionAdmin)


# 注意，内联是在父模型（外键指定的模型）中编辑子模型
class RegionInline(admin.TabularInline):
    model = CommonRegion
    extra = 0
    fields = ('chr', 'start', 'end')


class GeneAdmin(BaseAdmin):
    list_display = ['id', 'name', 'ensembl_id', 'bio_type', 'strand', ]
    list_filter = ['status', 'created_time', 'bio_type', 'strand', ]
    search_fields = ['name', 'ensembl_id', 'bio_type', 'strand']
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'ensembl_id',),
                ('bio_type', 'strand',),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(Gene, GeneAdmin)


class GeneRegionAdmin(BaseAdmin):
    list_display = ['id', 'gene', 'region']
    list_filter = ['status', 'created_time', ]
    search_fields = ['gene', 'region']
    fieldsets = (
        (None, {
            'fields': (
                ('gene', 'region',),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(GeneRegion, GeneRegionAdmin)


class GeneExpressionAdmin(BaseAdmin):
    list_display = ['id', 'gene_name', 'bio_sample_name', ]
    # list_filter = ('status', 'created_time',)
    search_fields = ['gene_name', 'bio_sample_name', ]
    fieldsets = (
        (None, {
            'fields': (
                ('gene_name', 'bio_sample_name', 'expression_value',),
                # ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(GeneExpression, GeneExpressionAdmin)


class SNPAdmin(BaseAdmin):
    list_display = ['id', 'rs_id', 'region', ]
    list_filter = ['status', 'created_time']
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
    list_display = ['id', 'name']
    list_filter = ['status', 'created_time', 'name']
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
    list_display = ['id', 'sample_id', 'bio_sample_name', 'tissue_type', 'bio_sample_type', 'species', 'source']
    list_filter = ['status', 'created_time', 'tissue_type', 'bio_sample_type', 'species', 'source']
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
    list_display = [
        'id',
        'silencer_id',
        'region',
        'score',
        'strand',
    ]
    # 设置list_filter来激活管理更改列表页面右侧侧栏的过滤器
    list_filter = ['status', 'created_time', ]
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


class SilencerGeneAdmin(BaseAdmin):
    list_display = [
        'silencer',
        'gene_name',
        'gene_ensembl_id',
        'genomic_loci',
        'strategy',
        'sub_strategy',
        'distance_to_TSS'
    ]
    list_filter = [
        # 'status',
        # 'created_time',
        'strategy'
    ]
    search_fields = [
        'silencer',
        'gene_name',
        'gene_ensembl_id',
        'genomic_loci',
        'strategy',
        'sub_strategy',
        'distance_to_TSS'
    ]
    fieldsets = (
        (None, {
            'fields': (
                ('silencer', 'gene_name', 'gene_ensembl_id', 'genomic_loci',),
                ('strategy', 'sub_strategy', 'distance_to_TSS',),
                # ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(SilencerGene, SilencerGeneAdmin)


class SilencerTranscriptionFactorAdmin(BaseAdmin):
    list_display = ['silencer', 'transcription_factor', 'binding_site']
    list_filter = ['status', 'created_time']
    search_fields = ['silencer', 'transcription_factor', 'binding_site']
    fieldsets = (
        (None, {
            'fields': (
                ('silencer', 'transcription_factor', 'binding_site'),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(SilencerTranscriptionFactor, SilencerTranscriptionFactorAdmin)


class SilencerSNPAdmin(BaseAdmin):
    list_display = ['silencer', 'snp', 'variant']
    list_filter = ['status', 'created_time', 'variant']
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


silencer_atlas_site.register(SilencerSNP, SilencerSNPAdmin)


class SilencerCas9Admin(BaseAdmin):
    list_display = ['silencer', 'region']
    list_filter = ['status', 'created_time']
    search_fields = ['silencer', 'region']
    fieldsets = (
        (None, {
            'fields': (
                ('silencer', 'region'),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(SilencerCas9, SilencerCas9Admin)


class SilencerRecognitionFactorAdmin(BaseAdmin):
    list_display = ['silencer', 'recognition_factor', ]
    list_filter = ['status', 'created_time', 'recognition_factor']
    search_fields = ['silencer', 'recognition_factor', ]
    fieldsets = (
        (None, {
            'fields': (
                ('silencer', 'recognition_factor'),
                ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(SilencerRecognitionFactor, SilencerRecognitionFactorAdmin)


class SilencerSampleRecognitionFactorAdmin(BaseAdmin):
    list_display = ['silencer', 'recognition_factor', 'bio_sample_name', 'z_score', 'recognized']
    list_filter = [
        # 'status', 'created_time',
        'recognition_factor',
        'bio_sample_name',
    ]
    search_fields = ['silencer', 'recognition_factor', 'bio_sample_name', 'z_score', 'recognized']
    fieldsets = (
        (None, {
            'fields': (
                ('silencer', 'recognition_factor', 'bio_sample_name',),
                ('z_score', 'recognized',),
                # ('remarks', 'remarks_json', 'status'),
            )
        }),
    )


silencer_atlas_site.register(SilencerSampleRecognitionFactor, SilencerSampleRecognitionFactorAdmin)
