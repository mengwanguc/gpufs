# TODO

1. Evaluate grouping with different datasets and models
     - Imagenet
     - Openimages
     - ???

1. Implement grouping in Tensorflow
2. Study Nvidia dali sequantial load (mentioned in dnnstall paper)
3. Investigate if dali supports async pre-processing
4. Study dali's async cpu-to-gpu data transfer
5. Does the async data transfer still work if we apply interleaving scheduling? Investigate
6. We require users to modify their programs when applying preemptive scheduling. Can we avoid it? Can we do it in gpu level?
