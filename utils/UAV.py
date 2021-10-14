from utils import Communication
from utils import PID
from utils import Timer
import numpy as np

class UAV:
	def __init__(self, timer, env, id, leader_id, weight = 15, init_pos = [0.0, 0.0, 0.0], init_speed = [0.0, 0.0, 0.0], relative_pos = [0.0, 0.0, 0.0]) -> None:
		'''
		timer: The Global Timer
		id: UAV's ID
		weight: UAV's weight(kg)
		init_post: UAV's initialize position(x, y, z)(m)
		relative_pos: UAV's relative position with leader UAV(x, y, z)(m)
		init_speed: UAV's initialize speed(x, y, z)(m/s)
		'''
		self.id = id
		self.leader_id = leader_id
		self.timer = timer
		self.weight = weight

		self.poster = Communication.Poster(timer, id, env)
		self.reciver = Communication.Reciver(timer, id, env)
		self.pid = PID.Force_PID(timer)

		# (x, y, z)
		self.pos = np.float128(init_pos)
		self.speed = np.float128(init_speed)
		self.rel_pos = np.float128(relative_pos)

		self.current_time = timer.time
		self.last_time = self.current_time
		self.force = np.float128([0, 0, 0])
	
	def update_status(self):
		force = self.force
		self.last_time, self.current_time = self.current_time, self.timer.time
		dt = self.current_time - self.last_time
		a = force / self.weight
		self.pos = self.pos + self.speed * dt + 0.5 * a * (dt**2)
		self.speed = self.speed + a * dt

	def update_force(self, rec_force):
		"""
		force: The force that the UAV recived(x, y, z)(N)
		"""
		rec_force = np.float128(rec_force)
		need_force = self.get_virtual_gravitation()
		all_force = need_force + rec_force
		self.pid.set_force(need_force)
		self.pid.update(all_force)
		true_force = need_force + self.pid.get_fix_force()
		self.force = true_force
	
	def post(self):
		info = {}
		info["pos"] = self.pos
		info["speed"] = self.speed
		self.poster.pos(info)
	
	def get_virtual_gravitation(self, alpha=0.1, min_distance=0.0001):
		info = self.reciver.rec(self.leader_id)
		leader_pos  = info["pos"]
		except_pos = leader_pos + self.rel_pos

		vec = except_pos - self.pos
		distance = np.sqrt(vec * vec).sum()
		if (distance > min_distance):
			vec = vec / distance
			gravitation = alpha * self.weight / (distance * distance)
			return vec * gravitation
		else:
			return np.float128([0, 0, 0])
	
