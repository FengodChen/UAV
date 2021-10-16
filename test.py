from utils.PID import PID
import random
from matplotlib import pyplot as plt
import numpy as np

pid = PID()
pid.clear()

now_value_list = []
pid_value_list = []
set_value_list = []
t = []
now_value = random.random()*2 - 1

for i in range(1, 101):
    i = i / 100
    set_value = (random.random() - 0.5) * 0.01
    pid.update_point(set_value)
    pid.update_time(i)
    pid.update(now_value)
    now_value_list.append(now_value)
    set_value_list.append(set_value)
    pid_value_list.append(pid.output)
    t.append(i)
    now_value = now_value + pid.output

now_value_list = np.array(now_value_list)
pid_value_list = np.array(pid_value_list)
t = np.array(t)

plt.subplot(1, 2, 1)
plt.plot(t, now_value_list)
plt.plot(t, set_value_list)
plt.title("Now Value")

plt.subplot(1, 2, 2)
plt.plot(t, pid_value_list)
plt.title("PID Value")

plt.show()
plt.savefig("a.jpg")