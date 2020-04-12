import numpy as np
import os
from pyidaungsu.dataInputStream import DataInputStream

class BinaryMarkov:
    def __init__(self,logProbabilityDifferences=None):
        self.logProbabilityDifferences = logProbabilityDifferences

        model_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'model/zawgyiUnicodeModel.dat')
        f = open(model_path, 'rb')
        dis = DataInputStream(f)
        
        size = 227
        logProbabilityDifferences = np.zeros((size, size))

        for ii1 in range(size):
            entries = dis.read_short()

            if (entries==0):
                fallback=0.0
            else:
                fallback=dis.read_float()

            nextt = -1

            for ii2 in range(size):
                if (entries > 0 and nextt < ii2):
                        nextt = dis.read_short()
                        entries=entries-1
                if (nextt == ii2):
                    logProbabilityDifferences[ii1][ii2] = dis.read_float()
                else:
                    logProbabilityDifferences[ii1][ii2] = fallback
                    
        logProbabilityDifferences = np.delete(logProbabilityDifferences, 0, 0)
        logProbabilityDifferences = np.delete(logProbabilityDifferences, 1, 0)
        logProbabilityDifferences = np.delete(logProbabilityDifferences, 2, 0)
        logProbabilityDifferences = np.delete(logProbabilityDifferences, 3, 0)
        self.logProbabilityDifferences = logProbabilityDifferences
    
    def getLogProbabilityDifference(self, prevState, currState):
        probability = self.logProbabilityDifferences[prevState][currState]

        # the state does not exist in the model, it will become multidimensional array instead of scalar value
        # in that case, return probability value = 0
        if probability.shape:
            return 0
        return probability