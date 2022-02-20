#本脚本非用来执行，而是应该复制粘贴到终端使用的
conda activate django
nohup python manage.py silencer_atlas_data --pre_update -f SilencerAtlas/libs/silencers.txt > pre_update_silencer_atlas_data.log 2>&1 &
nohup python manage.py silencer_atlas_update -s -f SilencerAtlas/libs/silencers.txt > silencer_atlas_data_update_silencers.log 2>&1 &
nohup python manage.py silencer_atlas_update -z -f SilencerAtlas/libs/recognition_factor_singles.txt > silencer_atlas_data_update_recognition_factor_singles.log 2>&1 &
nohup python manage.py silencer_atlas_update -r -f SilencerAtlas/libs/recognition_factor_classify.txt > silencer_atlas_data_update_recognition_factor_classify.log 2>&1 &
nohup python manage.py silencer_atlas_update -t -f SilencerAtlas/libs/target_genes.txt > silencer_atlas_data_update_target_genes.log 2>&1 &
echo "SilencerAtlas update done"