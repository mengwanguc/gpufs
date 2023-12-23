You need to using GPU node and CPU node. For the image you can use "Ubuntu20-Cuda11"

## Installing Fastflow in GPU node
1. Chameleon image

    Please use image "ubuntu20-xxx-cuda11-xxx."

    "xxx" means we don't care about what's there, as long as it's using ubuntu20 and cuda11.

2. Set up ssh
    ```
    ssh-keygen -t rsa -b 4096
    ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
    cat ~/.ssh/id_rsa.pub
    ```

    Copy and paste into: https://github.com/settings/keys

3. clone this repo to local

    ```
    git clone git@github.com:mengwanguc/gpufs.git
    cd gpufs
    git checkout naufal
    ```

4. Install conda

    ```
    wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
    bash Anaconda3-2021.11-Linux-x86_64.sh
    ```
    After installation, log out and log in bash again.

5. install bazelisk
    ```
    wget https://github.com/bazelbuild/bazelisk/releases/download/v1.8.1/bazelisk-linux-amd64
    chmod +x bazelisk-linux-amd64
    sudo mv bazelisk-linux-amd64 /usr/local/bin/bazel
        
    # make sure you get the binary available in $PATH
    which bazel
    ```

6. Instal cudnn cuda11
    ```
    gdown https://drive.google.com/uc?id=1VImNg43lxG1-eA6-j0kyb0x0y1asZ6E-
    tar xf cudnn-linux-x86_64-8.9.5.29_cuda11-archive.tar.xz 

    cd cudnn-linux-x86_64-8.9.5.29_cuda11-archive/
    sudo cp include/cudnn*.h /usr/local/cuda/include
    sudo cp lib/libcudnn* /usr/local/cuda/lib64
    sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
    ```

    to check cudnn installed or not:
    ```
    cat /usr/local/cuda/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
    ```
    it will produced :
    ```
    #define CUDNN_MAJOR 8
    #define CUDNN_MINOR 9
    #define CUDNN_PATCHLEVEL 5
    --
    #define CUDNN_VERSION (CUDNN_MAJOR * 1000 + CUDNN_MINOR * 100 + CUDNN_PATCHLEVEL)

    /* cannot use constexpr here since this is a C-only file */
    ```

7. Install tensorflow from source

    ```
    git clone https://github.com/SamsungLabs/fastflow-tensorflow.git
    cd fastflow-tensorflow/
    pip install -U --user keras_preprocessing --no-deps
    pip install -U --user keras_preprocessing --no-deps
    ./configure
    ```
    In configure you can just simply enter for every questions except for cuda because we have to enable it. 
    after you can install the tensorflow.

    ```
    bazel build //tensorflow/tools/pip_package:build_pip_package
    ./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg --project_name fastflow_tensorflow
    cd /tmp/tensorflow_pkg/
    pip install fastflow_tensorflow-2.7.0-cp39-cp39-linux_x86_64.whl
    ```

8. Instal Fastflow
    ```
    git clone https://github.com/SamsungLabs/FastFlow.git
    cd ~/FastFlow
    pip install -r ./requirements.txt
    ./build_pip_package.sh
    ```

9. Installing additional package

    ```
    cd ~/gpufs/Fastfloww/example
    pip install -r requirements_cuda11.txt
    pip install numpy --upgrade
    ```

10. training a model using fastflow.

    ```
    cd ~
    mkdir data
    cd ~/gpufs/Fastfloww/examples
    python eval_app_runner.py gan_ada_app.py /home/cc/data 'tf' default_config.yaml
    ```
    offloading_type:
    - 'tf': TensorFlow (no offloading) 
    - 'tf-dsr-all': TF+Remote Worker by offloading all operations (with dispatcher)
    - 'tf-dslr-all':TF+Local and Remote Worker by offloading all operations (with dispatcher)
    - 'dali': DALI
    - 'ff': FastFlow (with dispatcher)

    to using dipatcher you have to adjust dipatcher address in "default_config.yaml" into your cpu node address

11. emulate the GPU with CPU only

    copy custom fastflow file into their folders
    ```
    cp ~/gpufs/Fastfloww/engine-tf-fastflow/training.py /home/cc/anaconda3/lib/python3.9/site-packages/tensorflow/python/keras/engine/
    cp ~/gpufs/Fastfloww/fastflow-keras_utils/keras_utils.py /home/cc/anaconda3/lib/python3.9/site-packages/fastflow/
    ```
    run the script for CPU:
    ```
    cd ~
    mkdir data
    cd ~/gpufs/Fastfloww/examples
    python eval_app_runner.py gan_ada_app_cpu.py /home/cc/data 'tf' default_config.yaml
    ```


## Installing Dispatcher in CPU node

1. Chameleon image

    Please use image "ubuntu20-xxx-cuda11-xxx."

    "xxx" means we don't care about what's there, as long as it's using ubuntu20 and cuda11.

2. Set up ssh
    ```
    ssh-keygen -t rsa -b 4096
    ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
    cat ~/.ssh/id_rsa.pub
    ```

    Copy and paste into: https://github.com/settings/keys

3. clone this repo to local

    ```
    git clone git@github.com:mengwanguc/gpufs.git
    cd gpufs
    git checkout naufal
    ```

4. Install conda

    ```
    wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
    bash Anaconda3-2021.11-Linux-x86_64.sh
    ```
    After installation, log out and log in bash again.

5. install bazelisk
    ```
    wget https://github.com/bazelbuild/bazelisk/releases/download/v1.8.1/bazelisk-linux-amd64
    chmod +x bazelisk-linux-amd64
    sudo mv bazelisk-linux-amd64 /usr/local/bin/bazel
        
    # make sure you get the binary available in $PATH
    which bazel
    ```

6. Install tensorflow from source

    ```
    git clone https://github.com/SamsungLabs/fastflow-tensorflow.git
    cd fastflow-tensorflow/
    pip install -U --user keras_preprocessing --no-deps
    pip install -U --user keras_preprocessing --no-deps
    ./configure
    ```
    In configure you can just simply enter for every questions. We doesn't need cuda for dispatcher.  
    after you can install the tensorflow.

    ```
    bazel build //tensorflow/tools/pip_package:build_pip_package
    ./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg --project_name fastflow_tensorflow
    cd /tmp/tensorflow_pkg/
    pip install fastflow_tensorflow-2.7.0-cp39-cp39-linux_x86_64.whl
    ```

7. Adjust worker address.

    ```
    cd /home/cc/gpufs/Fastfloww/examples/dispatcher.py
    ```

    in this script you should change the ip address in worker_address variabel into public ip your gpu node.

8. Run dispatcher.py
    ```
    cd /home/cc/gpufs/Fastfloww/examples/
    python dispatcher.py
    ```





