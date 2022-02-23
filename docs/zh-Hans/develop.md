# 开发文档

## 注意事项

- 以下配置大部分需要root权限，请自行切换权限或者在命令前面加上**sudo**

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
            - 创建虚拟环境：`conda create -n django-backend python=3.10`
            - 激活虚拟环境：`conda activate django-backend`
            - 安装依赖：`pip install -r requirements-conda.txt`
                - 此处也可以直接使用`depends/requirements-pip.txt`安装依赖
    - 原生虚拟环境
        - 创建虚拟环境：`virtualenv -p python3.10 venv`
        - 激活虚拟环境：`source venv/bin/activate`
        - 安装依赖：`pip install -r depends/requirements-pip.txt`

## 项目启动（需要先激活虚拟环境）

- 推荐先进入项目文件夹`cd /.../Django-backend`
- 配置环境变量
    - `Django-backend/System`文件夹下创建`.env`文件
    - 配置`DJANGO_ENV`:`develop`或者`product`
    - 配置`HASHID_FIELD_SALT`:任意值
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
    - 全部修改完成后将配置链接到nginx的配置文件:`sudo ln -s /.../Django-abckend/System/nginx.conf /etc/nginx/conf.d/django-backend.conf`
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
    - 创建配置文件
        - `touch Django-backend/logs/supervisor/access.log`
        - `touch Django-backend/logs/supervisor/error.log`
    - 你可以选择使用默认的`/etc/supervisord.conf`和`/etc/supervisord.d`文件夹，或者像下面这样进行配置
    - 创建supervisor配置文件夹
        - `mkdir -p /etc/supervisor`
        - `mkdir -p /etc/supervisor/supervisord.d`
    - 备份supervisor配置文件：`echo_supervisord_conf > /etc/supervisor/supervisord.conf`
    - 修改supervisord.conf文件最后的include部分为：`files = /etc/supervisor/supervisord.d/*.ini`
    -
  链接本项目的supervisor配置文件：`sudo ln -s /.../Django-backend/System/supervisor.ini /etc/supervisor/supervisord.d/django-backend.ini`
    - 启动服务：`supervisord -c /etc/supervisor/supervisord.conf`

## 服务器

### 密钥文件

- 密钥文件用于ssh、上传文件使用：`wmu-sctpa.pem`
- 连接服务器：`ssh -i wmu-sctpa.pem wmu@sctpa.bio-data.cn`
    - 或者直接使用ip地址连接：`ssh -i wmu-sctpa.pem wmu@159.138.54.48`
    - 建议存放为sh文件，方便使用
        - 注意需要添加执行权限：`chmod +x ssh-wmu-sctpa.sh`
        - 启动：`./ssh-wmu-sctpa.sh`

### 资源文件

- 由于根目录下面的空间不够，故项目文件夹放至：`/data/Django-backend/`
    - 项目静态资源文件夹：`Django-backend/static/`
    - 项目媒体资源文件夹：`Django-backend/media/`
- 应用文件夹：`Django-backend/app_name/`

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