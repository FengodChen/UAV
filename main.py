from utils.UAV import UAV
from utils.Communication import Env
from utils.Timer import Timer

TIME_STEP = 0.001

init_time = 0.0
max_time = 3.0

timer = Timer()
env = Env(timer)

uav0 = UAV(timer, env, 0, 0, init_pos=[0, 0, 0], init_speed=[1, 1, 1], relative_pos=[0, 0, 0])
uav1 = UAV(timer, env, 1, 0, init_pos=[10, 0, 0], init_speed=[1, 1, 1], relative_pos=[10, 0, 0])
uav2 = UAV(timer, env, 2, 0, init_pos=[0, 10, 0], init_speed=[1, 1, 1], relative_pos=[0, 10, 0])
uav3 = UAV(timer, env, 3, 0, init_pos=[0, 0, 10], init_speed=[1, 1, 1], relative_pos=[0, 0, 10])

while init_time <= max_time:
    init_time += TIME_STEP
    timer.update(init_time)
    uav0.update_status()
    uav1.update_status()
    uav2.update_status()
    uav3.update_status()

    uav0.post()

    uav0.update_force([0, 0, 0])
    uav1.update_force([0, 0, 0])
    uav2.update_force([0, 0, 0])
    uav3.update_force([0, 0, 0])
