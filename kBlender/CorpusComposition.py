import numpy as np

class CorpusComposition:
    def __init__(self, vars, sizeAssembled, cathegorySizes, usedBounds, numTexts):
        self.vars = vars
        self.sizeAssembled = sizeAssembled
        self.cathegorySizes = cathegorySizes
        self.usedBounds = []
        self.numTexts = numTexts

        for b in usedBounds:
            self.usedBounds.append(np.round(b))

