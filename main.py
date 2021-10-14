from utils.UAV import UAV
from utils.Communication import Env
from utils.Timer import Timer
import numpy as np
from matplotlib import pyplot as plt

TIME_STEP = 0.0001

init_time = 0.0
max_time = 300.0

timer = Timer()
env = Env(timer)

uav0 = UAV(timer, env, 0, 0, init_pos=[0, 0, 0], init_speed=[1, 1, 1], relative_pos=[0, 0, 0])
uav1 = UAV(timer, env, 1, 0, init_pos=[10, 0, 0], init_speed=[1, 1, 1], relative_pos=[10, 0, 0])
uav2 = UAV(timer, env, 2, 0, init_pos=[0, 10, 0], init_speed=[1, 1, 1], relative_pos=[0, 10, 0])
uav3 = UAV(timer, env, 3, 0, init_pos=[0, 0, 10], init_speed=[1, 1, 1], relative_pos=[0, 0, 10])

def noise(t):
    if t < 200:
        return np.random.random(3) * 10 - 5
    else:
        return np.zeros(3)
    
t_list = []
distace_list = []

while init_time <= max_time:
    init_time += TIME_STEP
    timer.update(init_time)
    uav0.update_status()
    uav1.update_status()
    uav2.update_status()
    uav3.update_status()

    uav0.post()

    uav0.update_force([0, 0, 0])
    uav1.update_force(noise(init_time))
    uav2.update_force([0, 0, 0])
    uav3.update_force([0, 0, 0])

    t_list.append(init_time)
    distace_list.append(uav1.get_distance()[1])

t_list = np.array(t_list)
distace_list = np.array(distace_list)

plt.plot(t_list, distace_list)
plt.show()
