import numpy as np

class Graph:
    def __init__(self, vertices, adj, score):
        self.V = vertices + 1
        self.adj = [[] for i in range(vertices+1)]
        for index in range(self.V):
            self.adj[index] = adj[index].copy()
        self.adjNames = [[] for i in range(vertices+1)]
        self.score = score
    
    def __getRootNode(self):
        parentArray = np.full(self.V, -1)
        for parent in range(self.V):
            for child in self.adj[parent]:
                parentArray[child] = parent
        for index in range(self.V):
            if parentArray[index] == -1 and len(self.adj[index]) > 0:
                return index
        return -1
    
    def __printGraph(self, index, componentNames, printNames):
        neighbors = self.adj[index]
        if len(neighbors) == 0:
            return ""
        if printNames:
            strOut = str(componentNames[index]) + " -> " + self.__getLabelNeighbours(neighbors, componentNames) + ", "
        else:
            strOut = str(index) + " -> " + str(neighbors) + ", "
        for neighbor in neighbors:
            strOut = strOut + self.__printGraph(neighbor, componentNames, printNames)
        return strOut
    
    def __str__(self):
        startInd = self.__getRootNode()
        if startInd == -1:
            return f"adj={self.adj}"
        strOut = self.__printGraph(startInd, [], False)
        return strOut[:-2] + ", Score: " + str(self.score)
    
    def __getLabelNeighbours(self, neighbors, componentNames):
        strNeighbors = "["
        for neighbor in neighbors:
            strNeighbors = strNeighbors + componentNames[neighbor] + ", "
        return strNeighbors[:-2] + "]"
    
    def getStrAdj(self):
        for index in range(self.V):
            self.adj[index] = sorted(self.adj[index])
        return str(self.adj)
    
    def printLabelledGraph(self, componentNames):
        startInd = self.__getRootNode()
        if startInd == -1:
            return f"adj={self.adj}"
        strOut = self.__printGraph(startInd, componentNames, True)
        return strOut[:-2] + ", Score: " + str(self.score)
