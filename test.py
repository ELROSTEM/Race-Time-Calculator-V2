
import numpy as np


def total_time_gen(interval=0.0017):
    time = 0
    while time < 2:
        yield time
        time += interval


list = list(total_time_gen())

print(list)


# Create a list in a range of 10-20
My_list = np.arange(-3, 3, 0.5, dtype=float)
  
# Print the list
print(My_list)
