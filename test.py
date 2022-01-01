
def total_time_gen(interval=0.0017):
    time = 0
    while time < 2:
        yield time
        time += interval


list = list(total_time_gen())

print(list)
