import matplotlib.pyplot as plt

# Data
categories = ['FFCV' ,'ImageFolder']
values = [85, 315]

# Create a bar chart
plt.bar(categories, values)

# Adding labels and a title
plt.xlabel('Loader')
plt.ylabel('Training Time (sec/epoch)')
plt.title('comparison between the time to train one epoch on ImageNet')

# Save the chart as a JPG file
plt.savefig('figure5(a).jpg', format='jpg')

# Show the plot (optional)
# plt.show()
