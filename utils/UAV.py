from utils import Communication
from utils import PID
import numpy as np

__COMMUNICATION_ENV__ = Communication.Env()

class UAV:
	def __init__(self, id, weight = 15, init_pos = [0.0, 0.0, 0.0], init_speed = [0.0, 0.0, 0.0]) -> None:
		'''
		id: UAV's ID
		weight: UAV's weight(kg)
		init_post: UAV's initialize position(x, y, z)(m)
		init_speed: UAV's initialize speed(x, y, z)(m/s)
		'''
		self.id = id
		self.weight = weight

		self.poster = Communication.Poster(id, __COMMUNICATION_ENV__)
		self.reciver = Communication.Reciver(id, __COMMUNICATION_ENV__)
		self.pid = PID.Force_PID()

		# (x, y, z)
		self.pos = np.float128(init_pos)
		self.speed = np.float128(init_speed)

		self.cureent_time = 0.0
		self.last_time = self.cureent_time
	
	def update_time(self, current_time):
		self.cureent_time = current_time
	
	def update(self, force):
		"""
		force: The force that the UAV recived(x, y, z)(N)
		"""
		force = np.float128(force)
		dt = self.cureent_time - self.last_time
		a = force / self.weight
		self.pos = self.speed * dt + 0.5 * a * (dt**2)
		self.speed = self.speed + a * dt