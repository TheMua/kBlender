# -*- coding: utf-8 -*-
from __future__ import division
from kBlender.CathegoryTree import CathegoryTree
from kBlender.MetadataModel import MetadataModel
import time

start = time.time()

metaDB = '/opt/kontext-data/metadata/syn.db'
tableName = 'item'
corpusMaxSize = 20000000

cathegoryList = [
    [0, None, 1, None],
    [1, 0, 1/2, "opus_rokvyd <= 2000"],
    [2, 0, 1/2, "opus_rokvyd >= 2000"],

    [3, 1, 1/2, "opus_txtype_group == 'odborná'"],
    [4, 1, 1/2, "opus_txtype_group == 'beletrie'"]

]

cathegoryTree = CathegoryTree(cathegoryList, metaDB, tableName, corpusMaxSize)
mm = MetadataModel(cathegoryTree)


print("Executing the solver...")

corpusComposition = mm.solve()

if(corpusComposition.sizeAssembled > 0):
    print("Corpus composition successfull! \n")
    print("Selection size: \t %d" % corpusComposition.sizeAssembled)
    print("Number of texts: \t %d" % corpusComposition.numTexts)
    print("Cathegory sizes: \t " + str(corpusComposition.cathegorySizes))
    print("Used bounds: \t\t " + str(corpusComposition.usedBounds))

    i = 1
    f = open('output.txt', 'w+')
    for v in corpusComposition.vars:
        f.write("%d;%d \n" % (i,v))
        i = i + 1

else:
    print("Corpus composition failed. One of the provided conditions generates no data. ")



end = time.time()
print("Time taken: \t\t %d s" % (end - start))
