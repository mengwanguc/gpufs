### Emulate Salus for GPU Sharing 

1. Install depedency
    ```
    pip install pandas torch torchvision matplotlib
    ```

2. Get memory allocated and memory cache in a model.

    to get memory that has been used to train a model, you can use alexnet.py. this is will returned memory that are used to train a model for each job. This memory information will be used to see the minimum and maximum(peak) memory for salus emulation.

    ```
    cd ~/gpufs/log_gpumem_salus/src/
    python alexnet.py
    ```

3. Run single script for salus.

    in alexnet-salus-1.py it will emulate how the salus gpu sharing work using min and max memory from before. this gpu sharing will move to idle if theres occupied for gpu and if gpu mem allocated large than gpu limit. 

    this script will produce fps_log1.txt and time_log1.txt. fps_log1.txt is txt result for image per second in batch.  time_log1.txt is txt result for time needed for each batches.

    ```
    # this measurement for rtx6000
    # min_mem   = 553078784
    # max_mem   = 2447713280
    # limit_mem =   25396838400
    ```

    ```
    cd ~/gpufs/log_gpumem_salus/src/
    python alexnet-salus-1.py
    ```

4. Run 3 script at once

    this bash will run 3 script of alexnet-salus.py with different start time. alexnet-salus-1.py will be run immediately. alexnet-salus-2.py will be run after 15 second. and alexnet-salus-3.py will be run after 30.second.

    this script will produce fps_log.txt and time_log.txt for each script. fps_log.txt is txt result for image per second in batch.  time_log.txt is txt result for time needed for each batches.
    ```
    cd ~/gpufs/log_gpumem_salus/src/
    bash run-all.sh
    ```