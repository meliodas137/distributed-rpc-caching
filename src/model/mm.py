import sys
sys.path.append('../')

import itertools
import numpy as np
from graph import Graph
from typing import List
from parser.data_struct import Instruction

class MysteryMachine:

    def __init__(self, inputComponents, instructions):
        self.components = inputComponents
        self.instructions = instructions
        self.componentMap = {}
        self.componentIdToLabelMap = {}
        self.causalGraph = []
        self.observationGraph = []
        self.modelGraphs: Graph = []
        self.graphSet = set()
    

    def constructModel(self):
        self.__initializeDAG()
        self.__executeInstructions()

    def __initializeDAG(self):
        for i, string_value in enumerate(self.components):
            self.componentMap[string_value] = i
            self.componentIdToLabelMap[i] = string_value     
        n = len(self.components)
        self.causalGraph = np.ones((n, n), dtype=int)
        for i in range(n):
            self.causalGraph[i][i] = 0
        self.observationGraph = np.zeros((n, n), dtype=int)

    def __executeInstructions(self):
        for instruction in self.instructions:
            self.__executeInstruction(instruction)
        
    def __executeInstruction(self, instruction: Instruction):
        callerId = self.componentMap[instruction.caller]
        calleeId = self.componentMap[instruction.callee]
        self.causalGraph[calleeId][callerId] = 0
        self.observationGraph[callerId][calleeId] += 1

    def EnumeratePaths(self):
        n = len(self.components)
        nodeAdded = np.zeros(n, dtype=int)
        for index in range(n):
            nodeAdded[index] = 1
            adj = [[] for j in range(n)]
            self.__explorePaths(adj, index, 0, n, nodeAdded, 0)
            nodeAdded[index] = 0
        
        self.__printPaths()
        self.__filterPaths()
        print("Filtered Models: " + str(len(self.causalGraph)))
        self.__printPaths()
    
    def generateAllSets(self, nums: List[int]):
        subsets = []
        for L in range(0, len(nums)+1):
            for subset in itertools.permutations(nums, L):
                subsets.append(subset)
        return subsets

    # def __explorePaths2(self, adj, indexes, maxIndex, nodeAdded, score):
    #     notLeaf = False
    #     for currentIndex in indexes:
    #         avNums = []
    #         for index in range(maxIndex):
    #             if nodeAdded[index] == 0 and self.causalGraph[currentIndex][index] == 1:
    #                 avNums.append(index)
    #         combinations = self.generateAllSets(avNums)
    #         for combination in combinations:


    def __explorePaths(self, adj, currentIndex, minIndex, maxIndex, nodeAdded, score):
        # print(str(currentIndex) + ", " + str(parentIndex) + " -> " + str(nodeAdded))
        notLeaf = False
        for mode in range(3):
            for neighbor in range(max(0, minIndex), maxIndex):
                if self.causalGraph[currentIndex][neighbor] == 0 or nodeAdded[neighbor] == 1:
                    continue
                notLeaf = True
                if (mode == 0):
                    self.__explorePaths(adj, currentIndex, neighbor + 1, maxIndex, nodeAdded, score)
                edgeScore = self.observationGraph[currentIndex][neighbor]
                adj[currentIndex].append(neighbor)
                # print(f"mode={mode}, current={currentIndex}, neighbor={neighbor}, nodeAdded={nodeAdded}")
                nodeAdded[neighbor] = 1
                if mode == 1:
                    self.__explorePaths(adj, currentIndex, currentIndex, maxIndex, nodeAdded, score + edgeScore)
                else:
                    self.__explorePaths(adj, neighbor, currentIndex, maxIndex, nodeAdded, score+edgeScore)
                nodeAdded[neighbor] = 0
                adj[currentIndex].remove(neighbor)
        
        if not notLeaf:
            graph = Graph(maxIndex - 1, adj, score)
            strValue = graph.getStrAdj()
            if strValue not in self.graphSet:
                self.graphSet.add(strValue)
                self.modelGraphs.append(graph)
                # print("Graph added: " + str(adj))
            else:
                # print("Duplicate Graph: " + str(adj))
                pass

    def __printPaths(self):
        for graph in self.modelGraphs:
            print(graph)

    def __filterPaths(self):
        graphs = []
        for graph in self.modelGraphs:
            if graph.score != 0:
                graphs.append(graph)
        self.modelGraphs = graphs
    
    def chooseGraphModel(self):
        score = -1
        maxGraph = None
        for graph in self.modelGraphs:
            if graph.score > score:
                score = graph.score
                maxGraph = graph
        return maxGraph