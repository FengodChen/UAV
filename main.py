from utils.UAV import UAV_Follower, UAV_Leader
from utils.Timer import Timer
from utils.Noise import Noise
import numpy as np
from matplotlib import pyplot as plt

TIME_STEP = 0.00001

init_time = 0.0
max_time = 0.1

timer = Timer()

uav0 = UAV_Leader(timer, id=0, pid_sample_time=0.0001, init_pos=[0, 0, 0], init_speed=[1, 1, 1])
uav1 = UAV_Follower(timer, id=1, pid_sample_time=0.0001, relative_pos=[10, 0, 0], relative_speed=[0, 0, 0], true_pos=[10, 0, 0])
uav2 = UAV_Follower(timer, id=2, pid_sample_time=0.0001, relative_pos=[0, 10, 0], relative_speed=[0, 0, 0], true_pos=[0, 10, 0])
uav3 = UAV_Follower(timer, id=3, pid_sample_time=0.0001, relative_pos=[0, 0, 10], relative_speed=[0, 0, 0], true_pos=[0, 0, 10])



noise = Noise(timer, 0.01)

t_list = []
distace_list = []

while init_time <= max_time:
    init_time += TIME_STEP
    timer.update(init_time)

    uav0.update_status([0, 0, 0])
    uav1.update_status(noise.get_noise())
    uav2.update_status([0, 0, 0])
    uav3.update_status([0, 0, 0])

    t_list.append(init_time)
    distace_list.append(uav1.get_delta_pos()[1])

    uav1.fix_force()

t_list = np.array(t_list)
distace_list = np.array(distace_list)

plt.plot(t_list, distace_list)
plt.show()
