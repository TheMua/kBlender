# -*- coding: utf-8 -*-
from __future__ import division
from kBlender.CathegoryTree import CathegoryTree
from kBlender.MetadataModel import MetadataModel
import time

start = time.time()

metaDB = '/opt/kontext-data/metadata/syn.db'
tableName = 'item'

cathegoryList = [
    [0, None, 1, None],
    [1, 0, 1/3, ["opus_txtype_group", " == ", "publicistika"]],
    [2, 0, 1/3, ["opus_txtype_group", " == ", "beletrie"]],
    [3, 0, 1/3, ["opus_txtype_group", " == ", "odborná"]],
    [4, 1, 1/2, ["opus_rokvyd", " == ", "2002"]],
    [5, 1, 1/2, ["opus_rokvyd", " == ", "2003"]]
]

cathegoryTree = CathegoryTree(cathegoryList, metaDB, tableName)
mm = MetadataModel(cathegoryTree)


print("Executing the solver...")

corpusComposition = mm.solve()

if(corpusComposition.sizeAssembled > 0):
    print("Corpus composition successfull! \n")
    print("Selection size: \t %d" % corpusComposition.sizeAssembled)
    print("Number of texts: \t %d" % corpusComposition.numTexts)
    print("Cathegory sizes: \t " + str(corpusComposition.cathegorySizes))
else:
    print("Corpus composition failed. No data match one of the provided conditions. ")



end = time.time()
print("Time taken: \t\t %d s" % (end - start))
