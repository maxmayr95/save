import numpy as np;

class PIDController:

    def __init__(self):
        self.quality = 100
        self.sharpen = 0
        self.noise = 0
        self.size_error_prev = 0.0 # Error in previous frame size
        self.size_error_sum = 0.0  # Summation (Integral) of size error
        self.ssim_error_prev = 0.0 # Error in previous ssim value
        self.ssim_error_sum = 0.0  # Summation (Integral) of ssim error
        #self.file = open("debug.txt", "w")

    def compute_u(self, current_outputs, setpoints):
        self.compute_quality(current_outputs, setpoints)
        self.compute_sharpen(current_outputs, setpoints)
        noise = 0
        self.ctl = np.matrix([[self.quality], [self.sharpen], [noise]])
        return self.ctl
    
    def compute_quality(self, current_outputs, setpoints):
        K_p = 0.00001
        K_i = 0.00000001
        K_d = 0.000005
        error = setpoints.item(1) - current_outputs.item(1)
        self.size_error_sum += error
        error_diff = error - self.size_error_prev
        self.size_error_prev = error
        self.quality += K_p * error + K_i * self.size_error_sum + K_d * error_diff

        if (self.quality > 100):
            self.quality = 100
        elif (self.quality < 0):
            self.quality = 0

        #self.file.write("current_size=" + str(current_outputs.item(1)) + ", error=" + str(error) + ", sum=" + str(self.size_error_sum) + ", diff=" + str(error_diff) + ", ctrl=" + str(ctrl) +  ", quality=" + str(self.quality) + "\n")

    def compute_sharpen(self, current_outputs, setpoints):
        K_p = 100
        K_i = 1
        K_d = 20
        error = setpoints.item(0) - current_outputs.item(0)
        self.ssim_error_sum += error
        error_diff = error - self.ssim_error_prev
        self.ssim_error_prev = error
        self.sharpen += K_p * error + K_i * self.ssim_error_sum + K_d * error_diff

        if (self.sharpen > 5):
            self.sharpen = 5
        elif (self.sharpen < 0):
            self.sharpen = 0

        #self.file.write("current_ssim=" + str(current_outputs.item(0)) + ", error=" + str(error) + ", sharpen=" + str(self.sharpen) + "\n")