import numpy as np

class BangbangController:

    def __init__(self):
        self.quality = 100
        self.sharpen = 5
        self.noise = 5

    def compute_u(self, current_outputs, setpoints):
        if current_outputs.item(1) < setpoints.item(1):
            self.quality = 100 
        elif current_outputs.item(1) > setpoints.item(1):
            self.quality = 20 

        if current_outputs.item(0) < setpoints.item(0):
            self.sharpen = 5    # SSIMが低い場合、画像を鮮明化
            self.noise = 0      # SSIMを向上させるために、ノイズは減らす
        elif current_outputs.item(0) > setpoints.item(0):
            self.sharpen = 0    # SSIMが高い場合、追加の鮮明化は不要
            self.noise = 0      # ノイズは通常画質を損なうため、追加しない

        self.ctl = np.matrix([[self.quality], [self.sharpen], [self.noise]])
        return self.ctl
