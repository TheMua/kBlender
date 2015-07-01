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
    [4, 1, 1, ["opus_srclang", " == ", "CZE"]],
    [5, 1, 0, ["opus_srclang", " != ", "CZE"]],
    [6, 2, 1, ["opus_srclang", " == ", "CZE"]],
    [7, 2, 0, ["opus_srclang", " != ", "CZE"]],
    [8, 3, 1, ["opus_srclang", " == ", "CZE"]],
    [9, 3, 0, ["opus_srclang", " != ", "CZE"]]
]

cathegoryTree = CathegoryTree(cathegoryList, metaDB, tableName)
mm = MetadataModel(cathegoryTree)


print("Executing the solver...")

corpusComposition = mm.solve()

print(corpusComposition.sizeAssembled)
print(corpusComposition.cathegorySizes)
print(corpusComposition)

end = time.time()
print("Time taken: " + str(end - start) + "s")
