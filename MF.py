import numpy as np

class MF:
    def __init__(self, center, sigma):
        self.params ={
            'center': center,
            'sigma': sigma
        }

    def GetDegreeOfMembership(self, val):
        result = np.exp(
            (-(val - self.params['center'])** 2)/(2*self.params['sigma']**2)
        )
        return result