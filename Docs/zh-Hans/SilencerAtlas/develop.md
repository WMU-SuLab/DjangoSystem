# SilencerAtlas 开发文档

## home页面

- 图片大小
    - 保持16:9或者16:10的通用标准比例
        - 16:9：960x540,1920x1080,2880x1620,3840x2160,7680x4320
        - 16:10:960x600,1920x1200,2880x1800,3840x2400,7680x4800
    - 大小在0.5MB以内最佳，可以通过一些软件进行图片压缩，但是如果实在控制不了也可以大一些

## 数据库

### MySQL

- 创建迁移脚本：`python manage.py makemigrations`
- 迁移数据库：`python manage.py migrate --database=SilencerAtlas`

## 服务器

### 资源文件

- SilencerAtlas 应用资源文件夹：`Django-backend/SilencerAtlas/libs`
- 文件详细介绍
    - genome文件夹:bed文件，为genome browse页面服务
    - 初始化脚本文件
        - genes.bed:基因数据
        - sample_map.txt:样本对应的转换数据
        - gene_expressions.gct:基因-样本的表达数据，需要sample_map.txt中的数据转换样本名称
    - silencer文件
        - silencers.txt:silencer的主要数据，需要先运行预构建脚本
        - recognition_factor_singles.txt:识别因子的信号数据
        - recognition_factor_classify.txt:识别因子的分类数据
        - target_genes.txt:silencer靶基因相关的数据

### 数据处理

- 数据库注意事项
    - **请在导入数据的时候定时清理日志文件，否则会很快占满空间，导致数据库操作一直睡眠，不能继续导入**
- init
    - 初始化必须在正式导入数据前运行
    - 所有的命令在`Django-backend/silencer_atlas_init.sh`中
- import
    - 导入数据的命令在`Django-backend/silencer_atlas_update.sh`中