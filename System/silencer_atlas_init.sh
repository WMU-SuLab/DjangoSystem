#本脚本非用来执行，而是应该复制粘贴到终端使用的
conda activate django
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --database=SilencerAtlas
nohup python manage.py silencer_atlas_data --init > init_silencer_atlas_data.log 2>&1 &
echo 'SilencerAtlas init done'