# README
We use Resnet18 as an example in this README.


## When only 1 GPU is used

```
    elif args.gpu is not None:
        torch.cuda.set_device(args.gpu)
        model = model.cuda(args.gpu)
```

### What's `model`?

`model = models.__dict__[args.arch]()`

For Resnet18, `model = resnet18()` which is implemented in `torchvision-meng/torchvision/models/resnet.py`.

### How do we train the `model`

As is commonly known, when we train a Deep Learning model, we first perform "forward" to compute the outputs, 
and then perform "backward" to update the model. 

But if you search "forward" in the application script, you cannot find where it calls "forward". So you might be confused.

### Forward

If you look into the "train" function, for every batch, after the data is copied onto GPU, it calls `output = model(images)`.

Well you might ask: `model` here is an object of `Resnet` class, why can we use it like a function?

This is because here the `model` object is callable. If you don't know what's a callable object in Python, check this: https://realpython.com/python-callable-instances/

After you read the tutorial above, you will know that in order to make an object callable, we need to implement a `__call__` function. So where is
it implemented for `model`.

Well, note that `Resnet` is a subclass of `nn.Module`, which is implemented in `pytorch-meng/torch/nn/modules/module.py`.

And in `module.py`, you'll find `__call__ : Callable[..., Any] = _call_impl`

So when you call `output = model(images)`, you are actually calling `model(images)` -> `Resnet.__call__(images)` -> `nn.Module.__call__(images)`
-> `nn.Module._call_impl(images)`.

And inside `nn.Module._call_impl()`, you'll see it calls `self.forward()`, which in turn calls `Resnet.forward()`.


## DataParallel (multiple GPUs)

When args.gpu is not specified, the application will use all GPUs on the node to train
the model.

```
    elif args.gpu is not None:
        torch.cuda.set_device(args.gpu)
        model = model.cuda(args.gpu)
    else:
        # DataParallel will divide and allocate batch_size to all available GPUs
        if args.arch.startswith('alexnet') or args.arch.startswith('vgg'):
            model.features = torch.nn.DataParallel(model.features)
            model.cuda()
        else:
            model = torch.nn.DataParallel(model).cuda()
```

It will call `torch.nn.DataParallel` which is implemented in 
`pytorch-meng/torch/nn/data_parallel.py`

The comments say that 

> This container parallelizes the application of the given :attr:`module` by
    splitting the input across the specified devices by chunking in the batch
    dimension (other objects will be copied once per device). In the forward
    pass, the module is replicated on each device, and each replica handles a
    portion of the input. During the backwards pass, gradients from each replica
    are summed into the original module.

Basically, it converts `model` to `torch.nn.DataParallel(model)`.

Therefore, when `nn.Module._call_impl()` calls `forward`, it calls `nn.DataParallel.forward()`.

Inside `nn.DataParallel.forward()`, it first splits the input data into multiple parts, 
and assign each part to a model on a separate GPU. It then calls `Resnet.forward()` for each part.

## What we should study here

Assume when we use only 1 GPU, we set batch size to be 128. Suppose one batch takes 1 second on GPU.

When we use 2 GPUs, if we set batch size to be 256, then each GPU will need to compute 128 images.
How long will it take? Ideally it should still take 1 second, but usually it does not. Why?

- During forward, Pytorch splits data into multiple chunks, moves each chunk to a different GPU, and 
then perform forward. Splitting data add overheads, but moving multiple chunks in parallel might reduce
transfer time. So will forward time be longer or shorter or no effect? We need to measure.

- During the backward, gradients from each replica are summed into the original module. This introduces 
data communication/transfer overhead, which can make backward take longer time.

- Other factors...

Therefore, we need to measure the time cost for each step in order to make accurate emulation for data parallel training.