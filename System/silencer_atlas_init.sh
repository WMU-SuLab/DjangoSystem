conda activate django
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --database=SilencerAtlas
python manage.py silencer_atlas_data --init > init_data.log 2>&1
echo 'SilencerAtlas init done'