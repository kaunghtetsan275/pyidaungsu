from pyidaungsu.dataInputStream import DataInputStream
from pyidaungsu.binaryMarkov import BinaryMarkov
import math, os

class Detector:
    def __init__(self):
        # Standard Myanmar code point range before digits
        self.STD_CP0 = ord('\u1000')
        self.STD_CP1 = ord('\u103F')

        # Standard Myanmar code point range after digits
        self.AFT_CP0 = ord('\u104A')
        self.AFT_CP1 = ord('\u109F')

        # Extended Myanmar code point range A
        self.EXA_CP0 = ord('\uAA60')
        self.EXA_CP1 = ord('\uAA7F')

        # Extended Myanmar code point range B
        self.EXB_CP0 = ord('\uA9E0')
        self.EXB_CP1 = ord('\uA9FF')

        # Unicode space characters
        self.SPC_CP0 = ord('\u2000')
        self.SPC_CP1 = ord('\u200B')

        # Indices into Markov nodes
        self.STD_OFFSET = 1
        self.AFT_OFFSET = self.STD_OFFSET + self.STD_CP1 - self.STD_CP0 + 1
        self.EXA_OFFSET = self.AFT_OFFSET + self.AFT_CP1 - self.AFT_CP0 + 1
        self.EXB_OFFSET = self.EXA_OFFSET + self.EXA_CP1 - self.EXA_CP0 + 1
        self.SPC_OFFSET = self.EXB_OFFSET + self.EXB_CP1 - self.EXB_CP0 + 1
        self.END_OFFSET = self.SPC_OFFSET + self.SPC_CP1 - self.SPC_CP0 + 1

        '''
        * SSV: An ID representing which Unicode code points to include in the model:
        *
        * <p>SSV_STD_EXA_EXB_SPC - include Myanmar, Extended A, Extended B, and space-like
        * <p>STD_EXA_EXB - same as above but no space-like code points
        *
        * <p>"SSV" originally stands for State Set Version.
        *
        '''
        self.SSV_STD_EXA_EXB_SPC = 0
        self.SSV_STD_EXA_EXB = 1
        self.SSV_COUNT = 2
    
        BINARY_TAG = int(0x555A4D4F44454C20)

        model_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'model/zawgyiUnicodeModel.dat')
        f = open(model_path, 'rb')
        dis = DataInputStream(f)

        # Check magic number and serial version number
        binaryTag = dis.read_long()

        if (binaryTag != BINARY_TAG):
            print("Unexpected magic number; expected {} but got {}".format(BINARY_TAG, binaryTag))

        binaryVersion = dis.read_int()

        if (binaryVersion == 1):
            # Binary version 1 has no SSV field; SSV_STD_EXA_EXB_SPC is always used
            self.ssv = self.SSV_STD_EXA_EXB_SPC
        elif (binaryVersion == 2):
            # Binary version 2 adds the SSV field
            self.ssv = dis.read_int()
        else:
            print("Unexpected serial version number; expected 1 or 2 but got {}".format(binaryVersion))
    
    def getIndexForCodePoint(self, cp, ssv):
        if (self.STD_CP0 <= cp and cp <= self.STD_CP1):
            return cp - self.STD_CP0 + self.STD_OFFSET
        if (self.AFT_CP0 <= cp and cp <= self.AFT_CP1):
            return cp - self.AFT_CP0 + self.AFT_OFFSET
        if (self.EXA_CP0 <= cp and cp <= self.EXA_CP1):
            return cp - self.EXA_CP0 + self.EXA_OFFSET
        if (self.EXB_CP0 <= cp and cp <= self.EXB_CP1):
            return cp - self.EXB_CP0 + self.EXB_OFFSET
        if (self.ssv == self.SSV_STD_EXA_EXB_SPC and self.SPC_CP0 <= cp and cp <= self.SPC_CP1):
            return cp - self.SPC_CP0 + self.SPC_OFFSET
    
    def predict(self, string):
        prevCp = 0
        prevState = 0
        totalDelta = 0.0
        for i,offset in enumerate(string):
            if (i == len(string)-1):
                cp = 0
                currState = 0
            else:
                cp = ord(offset)
                currState = self.getIndexForCodePoint(cp, self.ssv)
            
            classifier = BinaryMarkov()
            if (prevState==None):
                continue
            if (prevState != 0 or currState != 0):
                delta = classifier.getLogProbabilityDifference(prevState, currState)
                totalDelta += delta

            prevCp = cp
            prevState = currState
        
        result = round(1.0/(1.0 + math.exp(totalDelta)))
        
        return result

    def detect(self, text):
        if self.predict(text):
            return "Zawgyi"
        else:
            return "Unicode"
        return "Other tongue"