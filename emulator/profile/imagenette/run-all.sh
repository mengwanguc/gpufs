gpu_type='k80'

models=(alexnet
         densenet121
         densenet161
         densenet169
         densenet201
         googlenet
         inception_v3
         mnasnet0_5
         mnasnet0_75
         mnasnet1_3
         mobilenet_v2
         mobilenet_v3_large
         mobilenet_v3_small
         resnet101
         resnet152
         resnet18
         resnet34
         resnet50
         resnext101_32x8d
         resnext50_32x4d
         shufflenet_v2_x0_5
         shufflenet_v2_x1_0
         shufflenet_v2_x1_5
         shufflenet_v2_x2_0
         squeezenet1_0
         squeezenet1_1
         vgg11
         vgg11_bn
         vgg13
         vgg13_bn
         vgg16
         vgg16_bn
         vgg19
         vgg19_bn
         wide_resnet101_2
         wide_resnet50_2
         )

batch_sizes=(64)

for model in ${models[@]}; do
    for batch_size in ${batch_sizes[@]}; do
        echo "Profiling for model $model with batch size $batch_size"
        python main-measure-time.py --epoch 1 ~/data/test-accuracy/imagenette2 --gpu 0 --gpu-type $gpu_type -a $model --batch-size $batch_size
        echo
    done
done



        


