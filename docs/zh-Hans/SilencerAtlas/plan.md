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

### 前端优化计划

- [x] 根据新模型重写所有页面
- [x] knockout.js替换为vue.js
- [x] 修复基因表达部分的echarts
- [ ] silencer details 界面剩余部分
- [x] 自己写一个异步下拉框处理数据量太大的问题
  - [x] 加载更多优化
  - [ ] 性能再优化

### 被搁置的计划

- 使用django-rest-framework
- [ ] 优化有外键关系的数据管理页面，使得二者或三者可以同时编辑

### 一些想法

- [ ] 把ManageSys文件夹修改为Manage