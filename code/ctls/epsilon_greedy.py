import numpy as np

def relu(x):
    return max(0, x)

class EpsGreedyController:
    def __init__(self):
        self.quality = 100 # generate random number
        self.sharpen = 0 # generate random number
        self.noise = 0 #generate random number
        self.state = {'error': [], 'quality': [], 'sharpen': [], 'noise': []}
    
    def compute_u(self, current_outputs, setpoints, epsilon):
        # error = relu(setpoints.item(0) - current_outputs.item(0)) + relu(current_outputs.item(1) - setpoints.item(1))
        self.state['error'].append(relu(setpoints.item(0) - current_outputs.item(0)) + relu(current_outputs.item(1) - setpoints.item(1)))
        self.state['quality'].append(self.quality)
        self.state['sharpen'].append(self.sharpen)
        self.state['noise'].append(self.noise)
        
        if np.random.random() < epsilon:
            self.quality = np.random.random_integers(1, 100) # generate random number
            self.sharpen = np.random.random_integers(0, 5) # generate random number
            self.noise = np.random.random_integers(0, 5) #generate random number
        else:
            j = np.argmin(self.state['error'])
            self.quality = self.state['quality'][j]
            self.sharpen = self.state['sharpen'][j]
            self.noise = self.state['noise'][j]

        self.ctl = np.matrix([[self.quality], [self.sharpen], [self.noise]])
        return self.ctl