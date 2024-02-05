gpu_type='p100'

models=(alexnet)
profile_batches=55

for model in ${models[@]}; do
    for batch_size in {176..176}; do
        echo "Profiling for model $model with batch size $batch_size"
        python main-measure-time.py --epoch 1 ~/data/test-util/imagenette2 --gpu 0 --gpu-type $gpu_type -a $model --batch-size $batch_size --profile-batches $profile_batches
        echo
    done
done
