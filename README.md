# DjangoSystem

## 文档

- [简体中文](README.md)
    - [详细文档](Docs/zh-Hans/index.md)
- [English](Docs/en-US/README.md)(todo)

## 说明

- 基于 Django 的后台管理系统
    - 可以整合多个**数据库和应用**，在一个服务器上运行
        - 应用不能使用自带的用户系统，因为Django难以在一个项目中用自带的用户管理系统实现多个应用互不相关的用户系统
        - 如果有用户管理需求，建议新建项目，而不是整合到现有的这个项目中
    - 目前整合的应用有：
        - [Silencer Atlas](Docs/zh-Hans/SilencerAtlas/README.md)

## 版权

- 基于[MIT 协议](LICENSE)

## 开发团队介绍

- 中国-温州医科大学-大数据研究所-功能基因组
    - [大数据研究所](http://www.ibbd.ac.cn/)
    - [功能基因组](https://yuan-group.github.io/)

### 文档更新记录

- 2021-10-30
    - 初始化文档
- 2022-01-06
    - 拆分中英文文档
    - 增加基础内容
- 2022-09-19
    - 增加应用相关说明