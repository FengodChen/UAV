class Timer:
	def __init__(self, init_time=0.0) -> None:
		self.time = init_time
	
	def update(self, time):
		self.time = time