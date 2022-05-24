## 版本改动

### SilencerAtlas

* v0.1:2021-10-30
    * 初步完成search和browse页面的功能
    * 完成了数据库的初步结构设计，编写了部分接口
    * 编写了数据导入和更新脚本的雏形，可快速更改
* v0.2:2021-12-03
    * 完成了genome browser、details界面雏形
    * details界面完成一半功能
* v0.2.1:2021-1-6
    * 多数据库支持基本完成
    * 数据库重构完成
    * 迁移至django-backend完成
* v0.2.2:2021-1-16
    * 重写了数据库构建脚本，完成了测试数据脚本的构建
* v0.2.3:2022-1-24
    * 增加了loading功能
    * 完善了home的搜索功能，并在search界面增加对应功能
    * 重构了几乎所有页面，用vue.js代替了knockout.js
    * 修复了browse界面错误的逻辑
    * 完成了初始化、更新、删除、导出等脚本，大幅度提高了性能
    * 修复了基因表达数据样本名称展示不全的问题
* v0.2.4:2022-1-26
    * 增加了gunicorn和nginx配置
    * 继续修复基因表达页面的展示问题
* v0.2.5:2022-1-29
    * 完成部署需要的各项配置文件
    * 完成数据库数据的迁移
    * 修复各项生产环境配置，完成所有需要的测试
    * 修复silencer details 页面echarts的展示数值问题和单选框显示不正确的问题
* v0.2.6:2022-1-31
    * 通过自己编写的异步查询输入选择框，成功解决性能问题
    * 切换bootcdn到jsdelivr，因为bootcdn有时候服务出错
* v0.2.7:2022-2-08
    * 优化searchSelect脚本
    * 完善SilencerAtlas说明文档
    * 添加supervisor配置文件
* v0.3.0:2022-2-19
    * 继续优化了searchSelect脚本，功能更强
    * 修复了browse页面边距的问题
    * 删除了tissue type相关的数据和展示
    * 完成了更新silencer的预构建脚本
        * 完成了更新silencer 信号和靶基因相关的脚本
        * 成功测试了各项脚本
        * 编写了在服务器上后台运行的shell脚本
    * 修复了silencer details页面的排序和数据展示选择框的bug
    * 重构了silencer target gene的数据库表结构
        * 根据新的数据结构完成了silencer details相关靶基因展示页面的重写
    * 完善了silencer details页面信号数据的展示
    * 各项性能优化和代码优化，大幅度增加速度
    * 完善表格数据展示的逻辑，最多选择前1000条展示
    * 服务器迁移数据库数据文件
    * 服务器迁移项目文件夹和需要导入的数据文件
    * 完成服务器环境的迁移
* v0.3.1:2022-2-20
    * 减少脚本中读取数据的行数
    * 完善数据处理shell脚本，但不是用于执行，而是复制粘贴到终端执行
* v0.3.2:2022-2-20
    * 修复gene name不是unique的问题
    * 优化数据库初始化脚本
* v0.3.3:2022-2-23
    * 完善初始化数据脚本
    * 通过构建命令基类给所有的脚本添加参数
    * 重新构建基因和区域的数据模型，改为多对多，修复bug和相应脚本
    * 重新构建基因表达数据模型，和基因模型解除关系
    * 调整原region为CommonRegion，继承自AbstractRegion，为后续可能的一对多关系做准备
    * 规范了模型命名，并调整了相应的admin部分
    * 处理silencer模型区域相关的问题
    * 增加home页面的图片，调整描述
    * 增加genome browse页面的一些数据
* v0.3.4:2022-2-28
    * 完成了所有导入脚本的测试，解决了MySQL大小写不敏感的问题
    * 完成了supervisor的测试
    * 完善了product的配置文件
    * 为genome browse页面增加选择展示功能，利用树形组件和自己编写的处理函数实现
    * 增加新版本的环境依赖文件
* v0.3.5:2022-3-12
    * 增加了邮件配置
    * 完善了首页文字对齐部分
    * 增加memcached数据库优化browse、search第一次的查询速度
    * 解决MySQL数据库日志问题
* v0.3.6:2022-3-18
    * 修改ManageSys为Manage，并修改相应脚本和配置
    * 修改Django-backend为DjangoSystem，并修改相应脚本和配置
    * 切换公用脚本和资源到Common文件夹下
    * 提取SilencerAtlas的middlewares,BaseModel,BaseAdmin等到公用工具中
    * 添加了Myopia App，做了一部分的配置
    * 修改了genome browse界面的树形组件的样式
    * 将数据库密码和SECRET_KEY相关配置数据移动到.env文件中
* v0.3.7:2022-3-23
    * 完成了silencer details页面的Nearby Genomic Features的html、js部分，等待数据文件以分析格式和调整数据库结构，完善查询语句
    * 删除SilencerSampleRecognitionFactor表中bio_sample_name的索引
