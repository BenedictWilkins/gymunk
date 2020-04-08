import numpy as np

def InformativeActionSpace(base_space, action_meanings, to_vec):
    return type(base_space.__name__, (base_space,), {'action_meanings':action_meanings, 
                                                    'to_vec':to_vec})

def onehotter(size):
    def funk(self, a):
        r = np.zeros(size)
        r[a] = 1.
        return r
    return funk