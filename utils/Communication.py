class Reciver:
	def __init__(self, timer, id, env) -> None:
		self.id = id
		self.env = env
		self.timer = timer
	
	def rec(self, id):
		return self.env.info[str(id)]

class Poster:
	def __init__(self, timer, id, env) -> None:
		self.id = id
		self.env = env
		self.timer = timer
	
	def pos(self, info):
		s = {str(self.id): info}
		self.env.update_info(s)

class Env:
	def __init__(self, timer) -> None:
		self.uav_list = []
		self.info = {}
		self.timer = timer
	
	def update_info(self, info):
		self.info.update(info)
	