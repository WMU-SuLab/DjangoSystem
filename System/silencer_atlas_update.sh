conda activate django
python manage.py silencer_atlas_data --pre_update -f SilencerAtlas/libs/silencers.txt > pre_update.log 2>&1
nohub python manage.py silencer_atlas_update -s -f SilencerAtlas/libs/silencers.txt > update_silencers.log 2>&1 &
nohub python manage.py silencer_atlas_update -z -f SilencerAtlas/libs/recognition_factor_singles.txt > update_recognition_factor_singles.log 2>&1 &
nohub python manage.py silencer_atlas_update -r -f SilencerAtlas/libs/recognition_factor_classify.txt > update_recognition_factor_classify.log 2>&1 &
nohub python manage.py silencer_atlas_update -t -f SilencerAtlas/libs/target_genes.txt > update_target_genes.log 2>&1 &
echo "SilencerAtlas update done"