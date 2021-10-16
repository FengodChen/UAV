from utils import PID
import numpy as np

class UAV:
    def __init__(self, timer, id, pid_sample_time = 0.001, weight = 15, pos = [0, 0, 0], speed = [0, 0, 0]) -> None:
        '''
        timer: The Global Timer
        id: UAV's ID
        weight: UAV's weight(kg)
        init_post: UAV's initialize position(x, y, z)(m)
        relative_pos: UAV's relative position with leader UAV(x, y, z)(m)
        init_speed: UAV's initialize speed(x, y, z)(m/s)
        '''
        self.id = id
        self.timer = timer
        self.weight = weight

        self.s_pid = PID.UAV_PID(timer, pid_sample_time)
        self.v_pid = PID.UAV_PID(timer, pid_sample_time)
        self.pid_sample_time = pid_sample_time

        self.s_pid.clear()
        self.v_pid.clear()

        self.pos = np.float128(pos)
        self.speed = np.float128(speed)
        self.force = np.float128([0, 0, 0])

        self.current_time = timer.time
        self.last_time = self.current_time
    
    def update_status(self, outside_force):
        outside_force = np.float128(outside_force)
        force = self.force + outside_force
        self.last_time, self.current_time = self.current_time, self.timer.time
        dt = self.current_time - self.last_time
        a = force / self.weight
        self.pos = self.pos + self.speed * dt + 0.5 * a * (dt**2)
        self.speed = self.speed + a * dt

class UAV_Leader(UAV):
    def __init__(self, timer, id, pid_sample_time, weight = 15, init_pos = [0.0, 0.0, 0.0], init_speed = [0.0, 0.0, 0.0]) -> None:
        '''
        timer: The Global Timer
        id: UAV's ID
        weight: UAV's weight(kg)
        init_post: UAV's initialize position(x, y, z)(m)
        relative_pos: UAV's relative position with leader UAV(x, y, z)(m)
        init_speed: UAV's initialize speed(x, y, z)(m/s)
        '''
        super().__init__(timer, id, pid_sample_time, weight, init_pos, init_speed)
    
    def get_status(self):
        return (self.pos, self.speed)
        

class UAV_Follower(UAV):
    def __init__(self, timer, id, pid_sample_time, weight = 15, relative_pos = [0.0, 0.0, 0.0], relative_speed = [0.0, 0.0, 0.0], true_pos = [0.0, 0.0, 0.0], true_speed = [0.0, 0.0, 0.0]) -> None:
       super().__init__(timer, id, pid_sample_time, weight, relative_pos, relative_speed)
       self.true_pos = np.float128(true_pos)
       self.true_speed = np.float128(true_speed)
       self.s_pid.set_true(self.true_pos)
       self.v_pid.set_true(self.true_speed)
    
    def fix_force(self):
        ds = self.s_pid.get_fix(self.pos)
        dv = self.s_pid.get_fix(self.speed)
        t = self.pid_sample_time
        self.force = self.weight * ((2 * ds) / (t**2) + dv / t)
    
    def get_delta_pos(self):
        vec = self.true_pos - self.pos
        distance = np.sqrt((vec * vec)).sum()
        return (vec, distance)
    
    def get_delta_speed(self):
        vec = self.true_speed - self.speed
        distance = np.sqrt((vec * vec)).sum()
        return (vec, distance)