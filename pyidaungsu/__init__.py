from pyidaungsu.detector import Detector
from pyidaungsu.binaryMarkov import BinaryMarkov
from pyidaungsu.dataInputStream import DataInputStream
from pyidaungsu import converter

import re

def cvt2zg(line):
    return converter.convert(line,'unicode','zawgyi')

def cvt2uni(line):
    return converter.convert(line,'zawgyi','unicode')

def syllabify(line):
    if (detect(line)=='Zawgyi'):
        line=converter.convert(line,'zawgyi','unicode')
    myConsonant = "က-အ"
    enChar = "a-zA-Z0-9"
    otherChar = "ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s"
    ssSymbol = '္'
    ngaThat = 'င်'
    aThat = '်'

    BreakPattern = re.compile("((?<!" + ssSymbol + ")["+ myConsonant + "](?![" + aThat + ssSymbol + "])" + "|[" + otherChar + "])", re.UNICODE)

    line = BreakPattern.sub(r" \1", line).strip()
    line = re.sub('(?<=[က-၏])([' +enChar+ '])',r' \1',line)
    line = re.sub('([0-9])\s+([0-9])\s*',r'\1\2',line)
    line = re.sub('([0-9])\s+(\+)',r'\1 \2 ',line)
    return line.split()

def detect(line):
    line = re.sub('[a-zA-Z0-9\+\-\s]','',line)
    if (len(line)>10):
        line = line[:10]
    return Detector().detect(line)
