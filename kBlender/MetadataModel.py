import sqlite3
import numpy as np
import pulp
from kBlender.CorpusComposition import CorpusComposition


class MetadataModel:
    def __init__(self, cathegoryTree):
        self.cTree = cathegoryTree
        self.connection = sqlite3.connect(self.cTree.metaDB)
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT COUNT(*) FROM %s" % self.cTree.tableName)
        self.numTexts = self.cur.fetchone()[0]
        self.b = [0]*(self.cTree.numCathegories-1)
        self.A = np.zeros((self.cTree.numCathegories,self.numTexts))
        self.__initAb(self.cTree.rootNode)
        self.textSizes = []

        for row in self.cur.execute("SELECT wordcount FROM item"):
            self.textSizes.append(row[0])


    def __initAb(self,node):
        sql = "SELECT id, wordcount FROM %s WHERE " % self.cTree.tableName;
        if(node.metadataCondition != None):
            i = 0
            for mc in node.metadataCondition:
                if(i > 0):
                    sql = sql + " AND "
                sql = sql + mc
                i = i + 1

            for row in self.cur.execute(sql):
                self.A[node.nodeId - 1][row[0]-1] = row[1]

            self.b[node.nodeId - 1] = node.size

        if(node.childs != []):
            for child in node.childs:
                self.__initAb(child)


    def solve(self):

        if(sum(self.b) == 0):
            return CorpusComposition(None, 0, None, [], 0)

        x_min = 0
        x_max = 1
        numConditions = len(self.b)
        x = pulp.LpVariable.dicts("x", range(self.numTexts), x_min, x_max)
        lp_prob = pulp.LpProblem("Minmax Problem", pulp.LpMaximize)
        lp_prob += pulp.lpSum(x), "Minimize_the_maximum"

        for i in range(0,numConditions):
            label = "Max_constraint_%d" % i
            condition = pulp.lpSum([self.A[i][j] * x[j] for j in range(self.numTexts)]) <= self.b[i]
            lp_prob += condition, label

        lp_prob.writeLP("MinmaxProblem.lp")  # optional
        lp_prob.solve()

        vars = [0] * self.numTexts
        #kind of ugly
        for v in lp_prob.variables():
            if(v.name == "__dummy"):
                continue
            i = int(v.name[2:len(v.name)])
            vars[i] = np.round(v.varValue, decimals=0)

        cathegorySizes = []
        for c in range(0, self.cTree.numCathegories-1):
            cSize = self.__getCathegorySize(vars, c)
            cathegorySizes.append(cSize)

        sizeAssembled = self.__getAssembledSize(vars)

        return CorpusComposition(vars, sizeAssembled, cathegorySizes, self.b, sum(vars))


    def __getAssembledSize(self, results):
        return np.dot(results, self.textSizes)

    def __getCathegorySize(self, results, catId):
        cathegorySizes = self.A[catId][:]
        return np.dot(results, cathegorySizes)



