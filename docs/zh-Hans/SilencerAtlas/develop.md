# SilencerAtlas 开发文档

## 服务器

- 由于根目录下面的空间不够，故项目文件夹放至：`/data/Django-backend/`
    - 项目静态资源文件夹：`/data/Django-backend/static/`
    - 项目媒体资源文件夹：`/data/Django-backend/media/`
    - SilencerAtlas 资源文件夹：`/data/Django-backend/SilencerAtlas/libs`

### 文件

- 上传文件之前请一定要注意磁盘空间是否足够，否则会导致上传失败。
- 上传文件：`scp -i wmu-sctpa.pem 文件路径 wmu@eyediseases.bio-data.cn:目标文件夹`
- 上传整个目录：`scp -i wmu-sctpa.pem -r 目录 wmu@eyediseases.bio-data.cn:目标文件夹`
