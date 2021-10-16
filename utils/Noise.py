import numpy as np

class Noise:
    def __init__(self, timer, step, k = 10, b = -5) -> None:
        self.step = step
        self.timer = timer
        self.last_update = 0.00
        self.k = k
        self.b = b
        self.noise = np.random.random(3) * k + b
    
    def get_noise(self):
        current_time = self.timer.time
        if (current_time - self.last_update > self.step):
            self.noise = np.random.random(3) * self.k + self.b
            self.last_update = current_time
        return self.noise