# SilencerAtlas

## 环境安装

- 基础环境（基础环境安装请自行搜索，不同操作系统有不同安装方法）
    - Python(3.9+)或者Conda(4.10+)
    - NGINX(1.20+)
    - MySQL(8.0+)
- 环境依赖文件位置
    - pipenv:`Django-backend/Pipfile`
    - conda
        - `Django-backend/depends/conda.yaml`
        - `Django-backend/depends/requirements-conda.txt`
    - pip:`Django-backend/depends/requirements-pip.txt`
- 首先需要进入项目文件夹：`cd Django-backend`
- 提供了以下几种环境安装方法
    - pipenv(推荐)
        - 安装pipenv：`pip install pipenv`
        - 安装依赖：`pipenv install`
    - conda
        - 使用导出的环境文件重建虚拟环境：`conda env create -f depends/conda.yaml`
        - 单独创建
            - 创建虚拟环境：`conda create -n django-backend python=3.9`
            - 激活虚拟环境：`conda activate django-backend`
            - 安装依赖：`pip install -r requirements-conda.txt`
                - 此处也可以直接使用`depends/requirements-pip.txt`安装依赖
    - 原生虚拟环境
        - 创建虚拟环境：`virtualenv -p python3.9 venv`
        - 激活虚拟环境：`source venv/bin/activate`
        - 安装依赖：`pip install -r depends/requirements-pip.txt`

## 项目启动（需要先激活虚拟环境）

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
    - 全部修改完成后将配置链接到nginx的配置文件:`sudo ln -s System/nginx.conf /etc/nginx/conf.d/django-backend.conf`
    - 启动NGINX：`sudo systemctl start nginx`
        - 或者`sudo service nginx start`
        - 如果已经启动，则重载配置：`sudo nginx -s reload`
- 配置MySQL(需要先启动并设置好用户名和密码)
    - 进入MySQL：`mysql -u root -p`
    - 创建数据库
        - `CREATE DATABASE DjangoAuth;`
        - `CREATE DATABASE SilencerAtlas;`
    - 配置`System/ManageSys/settings/product.py`
        - 修改`DATABASES`数据库用户和密码
    - 迁移数据库
        - `python manage.py makemigrations`
        - 创建表：`python manage.py migrate`
        - 创建DjangoAuth数据库表：`python manage.py migrate --database=DjangoAuth`
        - 创建SilencerAtlas数据库表：`python manage.py migrate --database=SilencerAtlas`
    - 创建django-admin的超级用户：`python manage.py createsuperuser`
- 配置gunicorn
    - 可以修改`System/gunicorn.py`文件中的端口等内容，默认不需要进行修改
- 配置supervisor
    - 创建supervisor配置文件夹
        - `mkdir -p /etc/supervisor`
        - `mkdir -p /etc/supervisor/supervisor.d`
    - 备份supervisor配置文件：`echo_supervisord_conf > /etc/supervisor/supervisord.conf`
    - 修改supervisord.conf文件最后的include部分为：`files = /etc/supervisor/supervisor.d/*.ini`
    -
  链接本项目的supervisor配置文件：`sudo ln -s /.../Django-backend/System/supervisor.ini /etc/supervisor/supervisor.d/django-backend.ini`
    - 启动服务：`supervisord -c /etc/supervisor/supervisord.conf`