# -*- coding: utf-8 -*-
from __future__ import division
from kBlender.CathegoryTree import CathegoryTree
from kBlender.MetadataModel import MetadataModel
from shutil import copyfile
import time
import sqlite3

start = time.time()

metaDB = '/opt/kontext-data/metadata/syn.db'
copyfile(metaDB, 'results.db')
tableName = 'item'
corpusMaxSize = 500000000

cathegoryList = [
    [0, None, 1, None],
    [1, 0, 1/2, "opus_rokvyd <= 2000"],
    [2, 0, 1/2, "opus_rokvyd >= 2000"],

    [3, 1, 1/2, "opus_txtype_group == 'odborná'"],
    [4, 1, 1/2, "opus_txtype_group == 'beletrie'"],

    [5, 2, 1/2, "opus_txtype_group == 'odborná'"],
    [6, 2, 1/2, "opus_txtype_group == 'beletrie'"]

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

    with sqlite3.connect('results.db') as con:
        cur = con.cursor()
        i = 1
        f = open('output.txt', 'w+')
        for v in corpusComposition.vars:
            f.write("%d;%d \n" % (i,v))

            if(v == 0):
                cur.execute("DELETE FROM %s WHERE id = %d;" % (cathegoryTree.tableName, i))

            i = i + 1

else:
    print("Corpus composition failed. One of the provided conditions generates no data. ")



end = time.time()
print("Time taken: \t\t %d s" % (end - start))
