# PyTorch index loading functions. There are enough of these that it was
# getting confusing to edit them in the main training script.

# All "load_indices" variants need to follow the same pattern. First, there must
# be a "front half", which initiates the loading (may be a no-op if the variant)
# does not require sending requests prior to reading back. Next, there must be a
# "back half", which reads back the files.

import os
import io
import time
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

## LADCACHE ##

def load_indices_ladcache_FRONT(cache, user_state, dataset, indices):
    # Request all of the images.
    for index in indices:
        path, _ = dataset.samples[index]
        queue_depth, in_flight = user_state.get_queue_depth(), user_state.get_in_flight()
        user_state.submit(path, retry=False)

def load_indices_ladcache_BACK(cache, user_state, dataset, indices):
    # Determine where all of the images belong.
    targets = {}
    for index in indices:
        path, target = dataset.samples[index]
        targets[path] = target

    # Wait for all of the images to be loaded.
    data = []
    for _ in indices:
        entry = user_state.reap(wait=True)
        filepath = entry.get_filepath().decode()
        data.append((targets[filepath], entry.get_data()))
        del entry # releases the entry

    return data

# Given separated front/back functions, generate a single combined function
def load_indices_front_back_wrapper(front, back):
    def temp(front, back, cache, user_state, dataset, batched_indices):
        front(cache, user_state, dataset, batched_indices)
        return [process_raw(dataset, raw, target) for target, raw in back(cache, user_state, dataset, batched_indices)]

    return partial(temp, front, back)

# Generic wrapper.
def load_indices_wrapper(cache, func):
    return partial(func, cache)