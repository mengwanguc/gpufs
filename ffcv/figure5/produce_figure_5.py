import matplotlib.pyplot as plt

# Data
categories = ['FFCV' ,'ImageFolder']
values = [92, 327]

# Create a bar chart
plt.bar(categories, values)

# Adding labels and a title
plt.xlabel('Loader')
plt.ylabel('Training Time (sec/epoch)')
plt.title('Comparison between the time to train one epoch on ImageNet (CPU-Resnet50)')

# Save the chart as a JPG file
plt.savefig('figure5(a)-cpu.jpg', format='jpg')

# Show the plot (optional)
# plt.show()
