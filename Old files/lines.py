# libraries and data
import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd

# evenly sampled time at 200ms intervals
x = [3, 5, 15.5, 20, 25, 35, 37, 46, 50, 52, 57]
#y = [0.5, 3, 3, 2.5, 1, 1, 0, 0, 4.5, 5, 5]
y = [10, 60, 60, 50, 20, 20, 0, 0, 90, 100, 100]

z = [3.5, 5, 15.5, 22, 25, 35, 37, 46, 50, 52, 57]
#w = [0.5, 2, 2, 2.5, 4, 4, 5, 5, 0.5, 0, 0]
w = [10, 40, 40, 50, 80, 80, 100, 100, 10, 0, 0]

# Add title and axis names
plt.title('Types of traffic in channel')
plt.xlabel('Time (Minutes)')
plt.ylabel('Channel occupancy (%)')

# red dashes, blue squares and green triangles
plt.plot(x, y, 'r', label = 'Payload')
plt.plot(z, w, 'y--', label = 'Dummy')

# Add legend
plt.legend(ncol=1)

plt.show()
