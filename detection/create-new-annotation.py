import os
import json
from collections import defaultdict

def load_annotations(ann_file):
    with open(ann_file, 'r') as f:
        annotations = json.load(f)
    return annotations

def create_subset_annotations(ann_file, num_train_images, num_val_images):
    # Load the annotations
    annotations = load_annotations(ann_file)

    # Get the first num_train_images for train subset
    train_subset = {
        'info': annotations['info'],
        'licenses': annotations['licenses'],
        'categories': annotations['categories'],
        'images': annotations['images'][:num_train_images],
        'annotations': []
    }

    # Get the first num_val_images for val subset
    val_subset = {
        'info': annotations['info'],
        'licenses': annotations['licenses'],
        'categories': annotations['categories'],
        'images': annotations['images'][:num_val_images],
        'annotations': []
    }

    # Create a mapping of image IDs to annotation IDs
    image_to_ann = defaultdict(list)
    for ann in annotations['annotations']:
        image_to_ann[ann['image_id']].append(ann)

    # Collect the annotations for the train subset
    for image in train_subset['images']:
        image_id = image['id']
        train_subset['annotations'].extend(image_to_ann[image_id])

    # Collect the annotations for the val subset
    for image in val_subset['images']:
        image_id = image['id']
        val_subset['annotations'].extend(image_to_ann[image_id])

    # Save the train annotations to a JSON file
    train_output_file = 'instances_train2017.json'
    with open(train_output_file, 'w') as f:
        json.dump(train_subset, f)

    # Save the val annotations to a JSON file
    val_output_file = 'instances_val2017.json'
    with open(val_output_file, 'w') as f:
        json.dump(val_subset, f)

# Paths to COCO dataset and annotations
ann_file = '/home/cc/mini-coco-dataset/coco_minitrain_25k/annotations/backup/instances_val2017.json'

# Specify the number of images for train and val subsets
num_train_images = 16
num_val_images = 4

# Create the subset annotations
create_subset_annotations(ann_file, num_train_images, num_val_images)