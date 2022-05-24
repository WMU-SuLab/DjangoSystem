# 说明

- 本文档不代表任何开发记录，也不代表任何任何开发版本，只是用来记录**一部分**的想法，不需要从本文档进行参考

# 计划

## 文档计划

- [ ] 详细开发文档
- [ ] 后端接口文档

## SilencerAtlas计划

### 后端优化计划

- [x] 最高优先级：browse页面逻辑修复
- [x] 重构项目，分模块，支持多应用多数据库
- [x] 数据库重构
- [x] 数据库脚本重构
- [x] gunicorn
- [x] NGINX
- [ ] 补全SNP、TFBs、基因相关的数据
- [x] 数据库迁移
- [x] 导入数据时候的silencer的查找不需要了，直接用索引
    - [x] 通过set集合减少查找内容
    - [x] 修复了索引的bug
    - [x] 通过字典映射大幅度优化查找速度
- [x] 有一些修饰需要大写显示
- [ ] 上传genome browse需要的数据
- [x] 导入新的较全的数据
    - [x] 测试导入silencer
    - [x] 测试导入修饰
    - [x] 测试导入靶基因
- [x] 迁移静态文件和资源文件到/data目录
- [x] 迁移数据库文件到/data/mysql目录
- [x] 删除tissue_type部分
- [ ] 优化数据库查询性能
    - [ ] 使用memcached缓存
    - [ ] 对视图进行缓存
- [x] 使用Supervisor管理
- [ ] SSL证书
- [ ] 域名

### 前端优化计划

- [x] 根据新模型重写所有页面
- [x] knockout.js替换为vue.js
- [x] 修复基因表达部分的echarts
- [ ] silencer details 界面剩余部分
  - [ ] Nearby Genomic Features
  - [ ] Cell Tissue Type Specificity
  - [ ] Linked Silencers In Other Assemblies
- [ ] home界面的新闻部分
- [ ] analysis
- [ ] statics
- [ ] contact
- [ ] help
- [ ] download
- [x] 自己写一个异步下拉框处理数据量太大的问题
    - [x] 加载更多优化
    - [x] 性能再优化
- [x] 增强genome browse页面的功能
  - [x] 修改样式为符合整体的风格

### 被搁置的计划

- [ ] 优化有外键关系的数据管理页面，使得二者或三者可以同时编辑
- [x] 重新导出多份Python环境文件

### 一些想法

- 名称变动
    - 因为设计到许多名字的变动，暂时是准备最后上线的时候再修改
    - [x] 把ManageSys文件夹修改为Manage
    - [x] 把Django-backend修改为DjangoSystem
    - [x] 把utils,template,static_dev迁移到Common文件夹中
