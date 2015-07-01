class CathegoryTreeNode:
    def __init__(self, nodeId, parentId, requestedRatio, metadataCondition):
        self.nodeId = nodeId
        self.parentID = parentId
        self.ratio = requestedRatio
        self.metadataCondition = metadataCondition
        self.size = None
        self.computedBounds = None

        self.childs = []
        