import json
import matplotlib.pyplot as plt
import numpy as np

train_top1, train_top5, val_top1, val_top5 = [],[],[],[]
train_top1_size2 = []
train_top1_size4 = []
train_top1_size8 = []
train_top1_size16 = []
train_top1_size32 = []
train_top1_size64 = []
epochs = 0
batch_size = 0
model = "M5"
batch_top1_top5 = {}
batch_top1_top5_size2 = {}
batch_top1_top5_size4 = {}
batch_top1_top5_size8 = {}
batch_top1_top5_size16 = {}
batch_top1_top5_size32 = {}
batch_top1_top5_size64 = {}


short_batch = '256'
current_p = 'AP'
current_title = 'Epoch related Accuracy Testing on Speech Command Dataset'
process = '_AP_'

with open('output_50epochs_M5_grouping_largedata_gsize64_nodataleakage.txt') as json_file:
    data = json.load(json_file)
    print(data, len(data))
    # print(type(data["AP"]))
    for k,v in data.items():
        if k == current_p:
            batch_top1_top5 = data["AP"]
        elif k == 'model':
            model = fasterrcnn_resnet50_fpn     
        elif k == 'args.epochs':
            epochs = 14	
        elif k == 'args.batch_size':
            batch_size = 2
    
    batch_top1_top5 = data["Accuracy"]
    batch_top1_top5 = [int(num * 100) for num in batch_top1_top5]
with open('output_50epochs_M5_nogrouping_largedata_2ndtry.txt') as json_file:
    data = json.load(json_file)
    for k,v in data.items():
        if k == current_p:
            batch_top1_top5_size2 = data[k]

    batch_top1_top5_size2 = data["Accuracy"]
    batch_top1_top5_size2 = [int(num * 100) for num in batch_top1_top5_size2]
with open('output_50epochs_M5_sequentialgrouping_largedata_gsize64_nodataleakage.txt') as json_file:
    data = json.load(json_file)
    for k,v in data.items():
        if k == current_p:
            batch_top1_top5_size4 = data[k]

    batch_top1_top5_size4 = data["Accuracy"]
    batch_top1_top5_size4 = [int(num * 100) for num in batch_top1_top5_size4]
# with open('output_50epochs_M5_sequentialgrouping_largedata_gsize64_shuffle-off.txt') as json_file:
#     data = json.load(json_file)
#     for k,v in data.items():
#         if k == current_p:
#             batch_top1_top5_size8 = data[k]
        
#     batch_top1_top5_size8 = data["Accuracy"]
#     batch_top1_top5_size8 = [int(num * 100) for num in batch_top1_top5_size8]

# with open('resnet18_batch_'+short_batch+'_gsize_16_epo_50') as json_file:
#     data = json.load(json_file)
#     for k,v in data.items():
#         if k == current_p:
#             batch_top1_top5_size16 = data[k]
# with open('resnet18_batch_'+short_batch+'_gsize_32_epo_50') as json_file:
#     data = json.load(json_file)
#     for k,v in data.items():
#         if k == current_p:
#             batch_top1_top5_size32 = data[k]
# with open('resnet18_batch_'+short_batch+'_gsize_64_epo_50') as json_file:
#     data = json.load(json_file)
#     for k,v in data.items():
#         if k == current_p:
#             batch_top1_top5_size64 = data[k]


def helper(batches):
    batch_range = []
    batch_top1, batch_top5 = [], []
    for k,v in batches.items():
        batch_range.append(int(k))
        batch_top1.append(v[0])
        batch_top5.append(v[1])
    return (batch_range, batch_top1, batch_top5)


# x1, top1s1, top5s1 = helper(batch_top1_top5)
# x2, top1s2, top5s2 = helper(batch_top1_top5_size2)
# x4, top1s4, top5s4 = helper(batch_top1_top5_size4)
# x8, top1s8, top5s8 = helper(batch_top1_top5_size8)
# x16, top1s16, top5s16 = helper(batch_top1_top5_size16)
# x32, top1s32, top5s32 = helper(batch_top1_top5_size32)
# x64, top1s64, top5s64 = helper(batch_top1_top5_size64)

epochs = 50
print("epoch ->", epochs)

epoch_range = range(1,epochs+1)
print("epoch_range ->", epoch_range)
plt.plot(epoch_range, batch_top1_top5_size2, label = 'no_grouping_bsize256', color="blue", linewidth=1)
plt.plot(epoch_range, batch_top1_top5_size4, label = 'sequentialgrouping_bsize256_gsize64', color="green", linewidth=1)
plt.plot(epoch_range, batch_top1_top5, '--', label = 'randgrouping_bsize256_gsize64', color="green", linewidth=3)
# plt.plot(epoch_range, batch_top1_top5_size8, '--', label = 'sequentialgrouping_bsize256_gsize64', color="red", linewidth=3)
# plt.plot(epoch_range, batch_top1_top5_size2, label = 'groupsize_2')
# plt.plot(epoch_range, batch_top1_top5_size4, label = 'groupsize_4')
# plt.plot(epoch_range, batch_top1_top5_size8, label = 'groupsize_8')
# plt.plot(epoch_range, batch_top1_top5_size16, label = 'groupsize_16')
# plt.plot(epoch_range, batch_top1_top5_size32, label = 'groupsize_32')
# plt.plot(epoch_range, batch_top1_top5_size64, label = 'groupsize_64')
plt.suptitle(current_title)
plt.title("(Model:M5, Lr:0.01)", fontsize=10)
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.xlim([0,epochs])
plt.ylim([0,100])
plt.legend()
plt.show(block=True) 
ep = str(epochs)
bat = str(batch_size)
results_dir = ''
sample_file_name = model+"_"+current_p + "_batch_" + bat +"_epo_"+ ep +"_nogrouping_randgrouping_sequential_bsize256_new"+".png" 
plt.savefig(results_dir + sample_file_name)

"""
plt.plot(x1, top1s1, label = 'groupsize_1')
plt.plot(x1, top1s2, label = 'groupsize_2')
plt.plot(x1, top1s4, label = 'groupsize_4')
plt.plot(x1, top1s8, label = 'groupsize_8')
plt.plot(x1, top1s16, label = 'groupsize_16')
plt.plot(x1, top1s32, label = 'groupsize_32')
plt.plot(x1, top1s64, label = 'groupsize_64')
plt.title(current_title)
plt.xlabel('Batch')
plt.ylabel('Accuracy')
plt.ylim([0,100])
plt.legend()
plt.show(block=True)
ep = str(epochs)
bat = str(batch_size)
results_dir = 'grouped_model_graph/'
sample_file_name = "batch_graph_"+ model +process+ "_batch_" + bat +"_epo_"+ ep +".png" 
plt.savefig(results_dir + sample_file_name)
"""