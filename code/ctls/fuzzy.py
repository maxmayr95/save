import numpy as np

class FuzzyController:
    def __init__(self):
        # Initialize control parameters
        self.quality = 100
        self.sharpen = 5
        self.noise = 5

    def compute_u(self, current_quality, current_size, setpoint_quality, setpoint_compression):
        # Quality adjustment
        quality_adjustment = self.compute_quality_adjustment(current_quality, setpoint_quality)
        new_quality = np.clip(current_quality + quality_adjustment, 1, 100)

        # Sharpen adjustment
        new_sharpen = self.compute_sharpen(current_size, setpoint_compression)

        # Noise adjustment
        new_noise = self.compute_noise(current_size, setpoint_compression)

        # Update control variables
        self.quality = new_quality
        self.sharpen = new_sharpen
        self.noise = new_noise

        # Create control matrix
        self.ctl = np.matrix([[self.quality], [self.sharpen], [self.noise]])
        return self.ctl

    def compute_quality_adjustment(self, current_quality, setpoint_quality):
        # Calculate quality adjustment based on the difference
        quality_diff = setpoint_quality - current_quality
        if quality_diff > 0.1:
            return 10
        elif quality_diff < -0.1:
            return -10
        else:
            return 0

    def compute_sharpen(self, current_size, setpoint_compression):
        # Calculate sharpen adjustment based on the size difference
        size_diff = setpoint_compression - current_size
        if size_diff > 1000:
            return 5
        elif size_diff < -1000:
            return 0
        else:
            return 3

    def compute_noise(self, current_size, setpoint_compression):
        # Calculate noise adjustment based on the size difference
        size_diff = setpoint_compression - current_size
        if size_diff > 1000:
            return 5
        elif size_diff < -1000:
            return 0
        else:
            return 3
