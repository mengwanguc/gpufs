gpu_type='v100'

models=(alexnet resnet18 mobilenet_v2)

batch_sizes=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 64 128 256)

for model in ${models[@]}; do
    for batch_size in ${batch_sizes[@]}; do
        echo "Profiling for model $model with batch size $batch_size"
        python main-measure-time.py --epoch 1 ~/data/test-accuracy/imagenette2 --gpu 0 --gpu-type $gpu_type -a $model --batch-size $batch_size
        echo
    done
done



        


