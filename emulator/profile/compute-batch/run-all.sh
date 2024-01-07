gpu_type='v100-cudnn'

models=(resnet50)
profile_batches=55

for model in ${models[@]}; do
    for batch_size in {1..256}; do
        echo "Profiling for model $model with batch size $batch_size"
        python main-measure-time.py --epoch 1 ~/data/imagenette2 --gpu 0 --workers 8 --gpu-type $gpu_type -a $model --batch-size $batch_size --profile-batches $profile_batches
        echo
    done
done
