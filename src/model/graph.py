import sys
sys.path.append('../')

import numpy as np
from typing import List
from parser.node import Node

class Graph:
    def __init__(self, vertices, adj, score):
        self.V = vertices + 1
        self.adj = [[] for i in range(vertices+1)]
        for index in range(self.V):
            self.adj[index] = adj[index].copy()
        self.adjNames = [[] for i in range(vertices+1)]
        self.score = score
    
    def getRootNode(self):
        parentArray = np.full(self.V, -1)
        for parent in range(self.V):
            for child in self.adj[parent]:
                parentArray[child] = parent
        for index in range(self.V):
            if parentArray[index] == -1 and len(self.adj[index]) > 0:
                return index
        return -1
    
    def getStrAdj(self):
        for index in range(self.V):
            self.adj[index] = sorted(self.adj[index])
        return str(self.adj)
    
    
    #################################################################    PRINTING    ############################################################
    
    def printLabelledGraph(self, componentNames):
        startInd = self.getRootNode()
        if startInd == -1:
            return f"adj={self.adj}"
        strOut = self.__printGraph(startInd, componentNames, True)
        return strOut[:-2] + ", Score: " + str(self.score)
    
    def __getLabelNeighbours(self, neighbors, componentNames):
        strNeighbors = "["
        for neighbor in neighbors:
            strNeighbors = strNeighbors + componentNames[neighbor] + ", "
        return strNeighbors[:-2] + "]"
    
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
        startInd = self.getRootNode()
        if startInd == -1:
            return f"adj={self.adj}"
        strOut = self.__printGraph(startInd, [], False)
        return strOut[:-2] + ", Score: " + str(self.score)


class NodeGraph:
    def __init__(self, nodes: List[Node], graph: Graph):
        self.nodes: List[Node] = nodes
        self.graph: Graph = graph
        self.__createNodeGraph()
        self.propagateDeterminism()
    
    def __createNodeGraph(self):
        for index in range(self.graph.V):
            self.__createNodeGraphIndex(index)

    def __createNodeGraphIndex(self, index):
        parentNode = self.nodes[index]
        for index in self.graph.adj[index]:
            parentNode.childNodes.append(self.nodes[index])

    def propagateDeterminism(self):
        undeter = np.full(len(self.nodes), -1)
        for node in self.nodes:
            if self.__checkNodeUndeterministic(node, undeter):
                node.deterministic = False

    def __checkNodeUndeterministic(self, node: Node, undeter: List[int]):
        if undeter[node.id] == 1:
            return True
        if undeter[node.id] == 0:
            return False
        if not node.deterministic:
            undeter[node.id] = 1
            return True
        for nbNode in node.childNodes:
            if self.__checkNodeUndeterministic(nbNode, undeter):
                undeter[node.id] = 1
                return True
        undeter[node.id] = 0
        return False


    #################################################################    PRINTING    ############################################################

    def __printNodeValue(self, node: Node):
        return "(ID: " + str(node.id) + ", Name: " + node.serviceName + ", Det: " + str(node.deterministic) + ")"

    def __printNode(self, node: Node):
        strOut = self.__printNodeValue(node) + " --> [ "
        for nbNode in node.childNodes:
            strOut = strOut + self.__printNodeValue(nbNode) + ", "
        return strOut[:-2] + " ]"
    
    def __printGraph(self, node: Node):
        nbNodes = node.childNodes
        if len(nbNodes) == 0:
            return ""
        strOut = self.__printNode(node)
        for nbNode in nbNodes:
            strOut = strOut + self.__printGraph(nbNode)
        return strOut


    def __str__(self):
        startInd = self.graph.getRootNode()
        strOut = self.__printGraph(self.nodes[startInd])
        return strOut