# PyTorch index loading functions. There are enough of these that it was
# getting confusing to edit them in the main training script.

# All "load_indices" variants need to follow the same pattern. First, there must
# be a "front half", which initiates the loading (may be a no-op if the variant)
# does not require sending requests prior to reading back. Next, there must be a
# "back half", which reads back the files.

import io
import minio
import time
import AsyncLoader as al
from functools import partial
from PIL import Image

# Convert from raw bytearray and target to usable data
def process_raw(dataset, raw, target):
    # t = time.time()
    sample = Image.open(io.BytesIO(raw)).convert('RGB')
    # print("\tto PIL image = {:.04}s".format(time.time() - t))

    if dataset.transform is not None:
        # t = time.time()
        sample = dataset.transform(sample)
        # print("\ttransform sample = {:.04}s".format(time.time() - t))
    if dataset.target_transform is not None:
        # t = time.time()
        target = dataset.target_transform(target)
        # print("\ttransform target = {:.04}s".format(time.time() - t))

    return sample, target


## PURE MINIO ##

def load_indices_minio_FRONT(cache, user_state, dataset, batched_indices):
    pass

def load_indices_minio_BACK(cache, user_state, dataset, batched_indices):
    data = []
    for i, indices in enumerate(batched_indices):
        data.append([])
        for index in indices:
            path, target = dataset.samples[index]
            data[i].append((target, cache.read(path)[0]))
    
    return data


## PURE ASYNC ##

def load_indices_async_FRONT(cache, user_state, dataset, batched_indices):
    # Request all of the images.
    for i, indices in enumerate(batched_indices):
        for index in indices:
            path, _ = dataset.samples[index]
            user_state.request(path)

def load_indices_async_BACK(cache, user_state, dataset, batched_indices):
    # Determine where all of the images belong.
    targets = {}
    path_to_batch = {}
    for i, indices in enumerate(batched_indices):
        for index in indices:
            path, target = dataset.samples[index]
            path_to_batch[path] = i
            targets[path] = target

    # Wait for all of the images to be loaded.
    data = [[] for _ in batched_indices]
    for i, indices in enumerate(batched_indices):
        for _ in indices:
            entry = user_state.wait_get()
            filepath = entry.get_filepath().decode()
            data[path_to_batch[filepath]].append((targets[filepath], entry.get_data()))
            entry.release()
    
    return data


## ASYNC AND MINIO ##

def load_indices_async_minio_FRONT(cache, user_state, dataset, batched_indices):
    # Request all of the images that aren't cached.
    for i, indices in enumerate(batched_indices):
        for index in indices:
            path, _ = dataset.samples[index]
            if not cache.contains(path):
                user_state.request(path)

def load_indices_async_minio_BACK(cache, user_state, dataset, batched_indices):
    # Determine where all of the images belong.
    cached, not_cached = [], []
    targets, path_to_batch = {}, {}
    for i, indices in enumerate(batched_indices):
        for index in indices:
            path, target = dataset.samples[index]
            path_to_batch[path] = i
            targets[path] = target
            if cache.contains(path):
                cached.append(path)
            else:
                not_cached.append(path)

    # Load the cached data.
    data = [[] for _ in batched_indices]
    for path in cached:
        data[path_to_batch[path]].append((targets[path], cache.load(path)[0]))
    
    # Wait for all of the images to be loaded.
    for i, indices in enumerate(batched_indices):
        for _ in indices:
            entry = user_state.wait_get()
            filepath = entry.get_filepath().decode()
            data[path_to_batch[filepath]].append((targets[filepath], entry.get_data()))
            entry.release()
    
    return data

## LADCACHE ##

def load_indices_ladcache_FRONT(cache, user_state, dataset, batched_indices):
    # Request all of the images.
    for i, indices in enumerate(batched_indices):
        for index in indices:
            path, _ = dataset.samples[index]
            user_state.submit(path)

def load_indices_ladcache_BACK(cache, user_state, dataset, batched_indices):
    # Determine where all of the images belong.
    targets = {}
    path_to_batch = {}
    for i, indices in enumerate(batched_indices):
        for index in indices:
            path, target = dataset.samples[index]
            path_to_batch[path] = i
            targets[path] = target

    # Wait for all of the images to be loaded.
    data = [[] for _ in batched_indices]
    for i, indices in enumerate(batched_indices):
        for _ in indices:
            entry = user_state.reap(wait=True)
            filepath = entry.get_filepath().decode()
            data[path_to_batch[filepath]].append((targets[filepath], entry.get_data()))
            del entry # releases the entry
    
    return data


# Generic wrapper.
def load_indices_wrapper(cache, func):
    return partial(func, cache)