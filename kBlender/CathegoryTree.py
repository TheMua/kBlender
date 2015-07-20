from kBlender.CathegoryTreeNode import CathegoryTreeNode
import numpy as np
import sqlite3

class CathegoryTree:
    """
    Cathegory tree represents the user required corpus structure

    :cathegoryList: A list of cathegories from which the user wants to generate the corpus including the requested ratios and links to their parent cathegories
    :metaDB: Path to file containing the Sqlite3 metadata database.
    :tableName: Name of the table in metaDB that holds the metadata
    :corpusMaxSize: Maximal size of resulting corpora in words

    """
    def __init__(self, cathegoryList, metaDB, tableName, corpusMaxSize):
        self.cathegoryList = cathegoryList
        self.numCathegories = len(cathegoryList)
        self.metaDB = metaDB
        self.tableName = tableName
        self.corpusMaxSize = corpusMaxSize
        self.rootNode = CathegoryTreeNode(self.cathegoryList[0][0], self.cathegoryList[0][1], self.cathegoryList[0][2], self.cathegoryList[0][3])
        self.connection = sqlite3.connect(self.metaDB)
        self.cur = self.connection.cursor()

        self.build()
        self.initializeBounds()

    def build(self):
        for i in range(1,len(self.cathegoryList)):
            cat = self.cathegoryList[i]
            nodeId = cat[0]
            parentId = cat[1]
            mc = cat[3]
            parentNode = self.__getNodeById(self.rootNode, parentId)
            pmc = parentNode.metadataCondition
            if(pmc != None):
                res = [mc] + pmc
            else:
                res = [mc]
            catNode = CathegoryTreeNode(nodeId, parentId, cat[2], res)

            parentNode.childs.append(catNode)


    def __getNodeById(self, node, wantedId):
        if(node.nodeId != wantedId):
            if(node.childs != None):
                for child in node.childs:
                    node = self.__getNodeById(child, wantedId)
                    if(node != None):
                        if(node.nodeId == wantedId):
                            return node
        else:
            return node

    def __getMaxGroupSizes(self, sizes, ratios, parentSize):
        numG = len(sizes)
        childsSize = sum(sizes)
        dataSize = min(childsSize, parentSize)
        wantedSizes = [0]*numG
        while(1):
            for i in range(0, numG):
                wantedSizes[i] = dataSize * ratios[i]

            reserves = np.subtract(sizes, wantedSizes)
            ilr = list(reserves).index(min(reserves))
            lovestReserve = reserves[ilr]
            if(lovestReserve > -0.001):
                maxSizes = wantedSizes
                break

            M = np.zeros((numG + 1, numG))
            for i in range(0, numG):
                row = (np.ones((1, numG)) * -ratios[i])[0]
                row[i] = 1 - ratios[i]
                M[i] = row

            M[numG, ilr] = 1
            b = np.zeros((numG + 1))
            b[numG]= sizes[ilr]

            maxSizes =  np.linalg.lstsq(M, b)[0]
            dataSize = sum(maxSizes)

        return maxSizes

    def computeSizes(self, node):
        if(node.childs != []):
            sizes = []
            ratios = []
            for child in node.childs:
                self.computeSizes(child)
                sizes.append(child.size)
                ratios.append(child.ratio)
            res = self.__getMaxGroupSizes(sizes, ratios, node.size)
            #update group size
            node.size = sum(res)
            #update child node sizes
            i = 0
            for n in node.childs:
                d = n.size - res[i]
                n.size = res[i]
                if(d > 0 and n.childs != []):
                    self.computeSizes(n)
                i = i + 1


    def initializeBounds(self):

        for i in range(1,len(self.cathegoryList)):
            node = self.__getNodeById(self.rootNode, i)
            categorySize = self.__getCategorySize(node.metadataCondition)
            node.size = categorySize

        sql = 'SELECT SUM(wordcount) FROM item '
        self.cur.execute(sql)
        maxAvailable = self.cur.fetchone()[0]

        self.rootNode.size = min(self.corpusMaxSize, maxAvailable)
        self.computeSizes(self.rootNode)

    def __getCategorySize(self, mc):
        """
        This method only computes the maximal available size of cathegory described by provided list of metadata conditions

        :mc: A list of metadata sql conditions that determines if texts belongs to this cathegory
        """

        sql = 'SELECT SUM(wordcount) FROM item WHERE '
        i = 0
        for c in mc:
            if(i > 0):
                sql = sql + " AND "
            sql = sql + c
            i = i + 1

        self.cur.execute(sql)
        size = self.cur.fetchone()[0]

        if(size == None):
            size = 0

        return size
