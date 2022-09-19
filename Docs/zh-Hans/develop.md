# 开发文档

## 注意事项

- 以下配置大部分需要root权限，请自行切换权限或者在命令前面加上**sudo**
- 项目根文件夹使用**ProjectRoot**代替

## 项目管理

- 新建项目：`django-admin startproject project_name`
- 新建app：`python manage.py startapp app_name`

## 环境

### 环境安装

- 基础环境（基础环境安装请自行搜索，不同操作系统有不同安装方法）
    - Python(3.9+)或者Conda(4.10+)
        - 本项目有部分命令使用了conda，可以替换为相应激活环境和安装包的方式
    - NGINX(1.20+)
    - MySQL(8.0+)
    - Supervisor(3.1+)
        - supervisor在不同的服务器的最新版本不同，但是使用Python安装的一定是最新的
    - Redis(4.0+)
    - Memcached(1.5+)
- 环境依赖文件位置
    - poetry:`ProjectRoot/pyproject.toml`
    - pipenv:`ProjectRoot/Pipfile`
    - conda
        - `ProjectRoot/depends/conda.yaml`
        - `ProjectRoot/depends/requirements-conda.txt`
    - pip:`ProjectRoot/depends/requirements-pip.txt`
- 提供了以下几种环境安装方法
    - 首先需要进入项目文件夹：`cd ProjectRoot`
    - poetry(推荐)
        - 安装 poetry：`pip install poetry`
        - 安装依赖：`poetry install`
        - 可在conda环境下使用
    - pipenv(推荐)
        - 安装 pipenv：`pip install pipenv`
        - 安装依赖：`pipenv install`
        - **不可在conda环境下使用**
    - conda
        - 使用导出的环境文件重建虚拟环境：`conda env create -f Dependencies/conda.yaml`
        - 单独创建
            - 创建虚拟环境：`conda create -n django python=3.10`
            - 激活虚拟环境：`conda activate django`
            - 安装依赖：`pip install -r requirements-conda.txt`
                - 此处也可以直接使用`Dependencies/requirements-pip.txt`安装依赖
        - 以上方法安装基本都会遇到各种各样的问题而失败，不如直接对照`Pipfile`文件一个一个手动安装
    - 原生虚拟环境
        - 创建虚拟环境：`virtualenv -p python3.10 venv`
        - 激活虚拟环境：`source venv/bin/activate`
        - 安装依赖：`pip install -r Dependencies/requirements-pip.txt`

### 环境导出

- 导出conda环境
    - `conda env export > conda.yaml`
    - `conda list -e > requirements-conda.txt`
- 导出pip环境：`pip freeze > requirements-pip.txt`
- pipenv, poetry, pdm 环境管理不需要导出，会自动写入配置文件

## 项目启动（需要先激活虚拟环境）

- 推荐先进入项目文件夹`cd /.../ProjectRoot`
- 配置环境变量
    - `ProjectRoot/System`文件夹下创建`.env`文件
    - 配置`DJANGO_ENV`:`develop`或者`product`
    - 配置加密，可以自己定义，但是最好查询各个字段官方的生成方法
        - 配置`SECRET_KEY`，django自带加密模块
        - 配置`CRYPTOGRAPHY_SECRET_KEY`，cryptography模块
        - 配置`HASHID_FIELD_SALT`，django-hashid-field插件
    - 配置邮箱
    - 配置数据库
        - MySQL
            - 根据是否使用多数据库添加其他数据库相应字段
        - Redis
        - Memcached

```dotenv
# .env文件示例
SECRET_KEY='django-insecure-k7t++81e%dpa!a^#2$7equ8+-=pu+52jf9x8bro#k2-k8!2n3e'
HASHID_FIELD_SALT='wmu-sulab-django-system'
CRYPTOGRAPHY_SECRET_KEY='no8tx8BM-bhPwSB-ud7sDXEg73eYFTaJqBJuS-qMKf8='

EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''

DJANGO_ENV='develop'
#DJANGO_ENV='product'

SERVER_DOMAIN='localhost'
SERVER_PORT='5000'

# Database
DATABASE_DEFAULT_PASSWORD=''
DATABASE_SILENCER_ATLAS_PASSWORD=''

```

- 创建日志文件夹
    - 使用`mkdir -p 路径`
        - django:`/.../ProjectRoot/System/logs/django`
        - gunicorn:`/.../ProjectRoot/System/logs/gunicorn`
        - supervisor:`/.../ProjectRoot/System/logs/supervisor`
        - NGINX:`/var/log/nginx`
    - 不需要创建对应的文件，配置文件里写好后这些都会自动创建文件
- 配置NGINX
    - 先收集静态文件:`python manage.py collectstatic`
    - 修改`nginx.conf`
        - 修改端口号
        - 修改域名或者ip地址
        - 修改用户名相关部分
        - 修改静态资源文件目录
        - 修改日志路径
        - 修改django服务器相关部分
        - 修改ssl相关配置
    -
  全部修改完成后将配置链接到nginx的配置文件:`sudo ln -s /.../ProjectRoot/System/nginx.conf /etc/nginx/conf.d/wmu-bio-data.conf`
    - 启动NGINX：`sudo systemctl start nginx`
        - 或者`sudo service nginx start`
        - 如果已经启动，则重载配置：`sudo nginx -s reload`
- 配置MySQL(需要先启动并设置好用户名和密码)
    - 进入MySQL：`mysql -u root -p`
    - 创建数据库：django对于除了sqlite的数据库都要求提前建好库
        - `CREATE DATABASE DjangoAuth;`
        - `CREATE DATABASE SilencerAtlas;`
        - 其余步骤自己查，或者用数据库管理工具建表，更加方便快速
        - ☆☆☆☆☆***一定要使用utf8mb4编码和utf8mb4_0900_as_cs排序规则，否则字段内容大小写不敏感，导致插入内容插插进去***
          ☆☆☆☆☆
    - 配置`System/Manage/settings/product.py`
        - 修改`DATABASES`数据库用户和密码
    - 迁移数据库
        - `python manage.py makemigrations`
        - 创建表：`python manage.py migrate`
        - 创建DjangoAuth数据库表：`python manage.py migrate --database=DjangoAuth`
        - 创建SilencerAtlas数据库表：`python manage.py migrate --database=SilencerAtlas`
    - 创建django-admin的超级用户：`python manage.py createsuperuser`
- 启动Memcached:`service memcached start`
    - `memcached -d -u root -l 127.0.0.1 -p 11211 -m 128`
- 配置gunicorn
    - 可以修改`System/gunicorn.py`文件中的端口等内容，默认不需要进行修改
        - 如果不准备使用supervisor可以将gunicorn改为后台运行
    - 创建日志文件
        - `touch ProjectRoot/logs/gunicorn/access.log`
        - `touch ProjectRoot/logs/gunicorn/error.log`
    - 启动：`gunicorn Manage.wsgi -c gunicorn.py`
- 配置supervisor
    - 创建日志文件
        - `touch ProjectRoot/logs/supervisor/access.log`
        - `touch ProjectRoot/logs/supervisor/error.log`
    - 你可以选择使用默认的`/etc/supervisord.conf`和`/etc/supervisord.d`文件夹，或者像下面这样进行配置
        - 创建supervisor配置文件夹
            - `mkdir -p /etc/supervisor`
            - `mkdir -p /etc/supervisor/supervisord.d`
    - 备份supervisor配置文件：`echo_supervisord_conf > /etc/supervisor/supervisord.conf`
    - 修改supervisord.conf文件最后的include部分为：`files = /etc/supervisor/supervisord.d/*.ini`
    -
  链接本项目的supervisor配置文件：`sudo ln -s /.../ProjectRoot/System/supervisor.ini /etc/supervisor/supervisord.d/wmu-bio-data.ini`
    - 启动服务：`supervisord -c /etc/supervisor/supervisord.conf`
        - 问题
            - BACKOFF Exited too quickly (process log may have details)
                - 根目录出错
                - 日志文件或者其目录不存在
            - 无法使用source等终端命令：使用bash -c "command"
            - 不断exit status 0; not expected
                - supervisor无法处理不在前台的程序，如nohup、gunicorn设置了守护进程等
                - 多次出现是因为没有监测到前台程序不断重启

## 服务器

### 密钥文件

- 密钥文件用于ssh、上传文件使用：`wmu-sctpa.pem`
    - 此文件必须运行权限设置：`chmod 400 wmu-sctpa.pem`，因为私钥权限设置的不能过于开放
    - 如果连接不了，请尝试使用`sudo`进行连接
- 连接服务器：`ssh -i wmu-sctpa.pem wmu@sctpa.bio-data.cn`
    - 或者直接使用ip地址连接：`ssh -i wmu-sctpa.pem wmu@159.138.54.48`
    - 建议存放为sh文件，方便使用
        - 注意需要添加执行权限：`chmod +x ssh-wmu-sctpa.sh`
        - 启动：`./ssh-wmu-sctpa.sh`
- 本地端口转发：`sudo ssh -L 本地端口:localhost:目标机服务器端口 跳板机服务器用户@跳板机服务器密码 -i 跳板机身份验证`
    - 可以百度和远程端口转发的区别
    - 如连接MySQL：`sudo ssh -L 33060:localhost:3306 -i wmu-sctpa.pem wmu@159.138.54.48`

### 资源文件

- 由于根目录下面的空间不够，故项目文件夹放至：`/data/ProjectRoot/`
    - 项目静态资源文件夹：`ProjectRoot/static/`
    - 项目媒体资源文件夹：`ProjectRoot/media/`
- 应用文件夹：`ProjectRoot/app_name/`

### 上传文件

- 上传文件之前请一定要注意磁盘空间是否足够，否则会导致上传失败
- 上传文件：`scp -i wmu-sctpa.pem 文件路径 wmu@eyediseases.bio-data.cn:目标文件夹`
- 上传整个目录：`scp -i wmu-sctpa.pem -r 目录 wmu@eyediseases.bio-data.cn:目标文件夹`

### 常用管理命令

- NGINX
    - 启动：service nginx start
    - 快速停止或关闭：nginx -s stop
    - 正常停止或关闭：nginx -s quit
    - 重启：service nginx restart
    - 重载：nginx -s reload
- MySQL
    - 启动：service mysqld start
    - 停止：service mysqld stop
    - 重启：service mysqld restart
    - 登录：mysql -uroot -p
- Supervisor
    - 启动Supervisor：supervisord -c /etc/supervisord.conf
        - 配置文件需要根据你设置的位置进行调整
    - 关闭supervisor：supervisorctl shutdown
    - 查看所有进程的状态：supervisorctl status
    - 启动服务：supervisorctl start 服务名
    - 停止服务：supervisorctl stop 服务名
    - 重启服务：supervisorctl restart 服务名
    - 重载配置：supervisorctl update
    - 重新启动配置中的所有程序：supervisorctl reload
    - 清空进程日志：supervisorctl clear 服务名
    - 服务名可以使用all代替所有服务
    - 启动supervisor并加载默认配置文件：systemctl start supervisord.service
    - 将supervisor加入开机启动项：systemctl enable supervisord.service