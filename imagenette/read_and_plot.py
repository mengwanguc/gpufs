import json
import matplotlib.pyplot as plt
import numpy as np

train_top1, train_top5, val_top1, val_top5 = [],[],[],[]
epochs = 0
batch_size = 0
model = ""
batch_top1_top5_train = {}
batch_top1_top5_val = {}

with open('resnet18/resnet18_batch_128_gsize_1_epo_50') as json_file:
    data = json.load(json_file)
    for k,v in data.items():
        if k == 'train_top1':
            train_top1 = data[k]
        elif k == 'train_top5':
            train_top5 = data[k]
        elif k == 'val_top1':
            val_top1 = data[k]
        elif k == 'val_top5':
            val_top5 = data[k]
        elif k == 'model':
            model = data[k]           
        elif k == 'args.epochs':
            epochs = data[k]	
        elif k == 'args.batch_size':
            batch_size = data[k]
        elif k == 'batch_acc_train':
            batch_top1_top5_train = data[k]
        elif k == 'batch_acc_val':
            batch_top1_top5_val = data[k]

batch_train_range, batch_val_range = [], []
batch_train_top1, batch_train_top5 = [], []
batch_val_top1, batch_val_top5 = [], []

for k,v in batch_top1_top5_train.items():
    batch_train_range.append(int(k))
    batch_train_top1.append(v[0])
    batch_train_top5.append(v[1])

for k,v in batch_top1_top5_val.items():
    batch_val_range.append(int(k))
    batch_val_top1.append(v[0])
    batch_val_top5.append(v[1])

#"""
epoch_range = range(1,epochs+1)
plt.plot(epoch_range, train_top1, label = 'train_top1')
plt.plot(epoch_range, train_top5, label = 'train_top5')
plt.plot(epoch_range, val_top1, label = 'val_top1')
plt.plot(epoch_range, val_top5, label = 'val_top5')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.ylim([0,100])
plt.legend()
plt.show(block=True) 
ep = str(epochs)
bat = str(batch_size)
results_dir = 'resnet18/'
sample_file_name = model+"_ec_" + "_batch_" + bat +"_epo_"+ ep +".png" 
plt.savefig(results_dir + sample_file_name)

"""
plt.plot(batch_train_range, batch_train_top1, label = 'train_top1_per100_batch')
plt.plot(batch_train_range, batch_train_top5, label = 'train_top5_per100_batch')
plt.plot(batch_val_range, batch_val_top1, label = 'val_top1_per100_batch')
plt.plot(batch_val_range, batch_val_top5, label = 'val_top5_per100_batch')
plt.title('Batch Related Training and Validation Accuracy')
plt.xlabel('Batch')
plt.ylabel('Accuracy')
plt.ylim([0,100])
plt.legend()
plt.show(block=True)
ep = str(epochs)
bat = str(batch_size)
results_dir = 'base_model_graph/'
sample_file_name = "batch_graph_"+ model + "_batch_" + bat +"_epo_"+ ep +".png" 
plt.savefig(results_dir + sample_file_name)
"""
