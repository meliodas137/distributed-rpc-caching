import sys
sys.path.append('../')

import numpy as np
from parser.data_struct import Instruction

class MysteryMachine:

    def __init__(self, inputComponents, instructions):
        self.components = inputComponents
        self.instructions = instructions
        self.componentMap = {}
        self.componentIdToLabelMap = {}
        self.causalGraph = []
        self.observationGraph = []
        self.causalPaths = []


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
            

    def __executeInstruction(self, instruction):
        callerId = self.componentMap[instruction.caller]
        calleeId = self.componentMap[instruction.callee]
        self.causalGraph[calleeId][callerId] = 0
        self.observationGraph[callerId][calleeId] += 1

    def EnumeratePaths(self):
        n = len(self.components)
        nodeAdded = np.zeros(n, dtype=int)
        for i in range(n):
            nodeAdded[i] = 1
            for j in range(n):
                currentPath = [i]
                if self.causalGraph[i][j] == 1:
                    currentPath.append(j)
                    nodeAdded[j] = 1
                    self.__explorePaths(currentPath, j, n, nodeAdded)
            nodeAdded[i] = 0
        
        self.__printPaths()
        print("Filtered Paths:")
        self.__filterPaths()

    def __explorePaths(self, currentPath, currentIndex, maxIndex, nodeAdded):
        notLeaf = False
        for i in range(maxIndex):
            if self.causalGraph[currentIndex][i] == 0 or nodeAdded[i] == 1:
                continue
            notLeaf = True
            currentPath.append(i)
            nodeAdded[i] = 1
            self.__explorePaths(currentPath, i, maxIndex, nodeAdded)
        
        if not notLeaf:
            self.causalPaths.append(list(currentPath))
        
        nodeAdded[currentIndex] = 0
        currentPath.pop()

    def __filterPaths(self):
        filterPaths = []
        for path in self.causalPaths:
            score = self.__getPathScore(path)
            if score > 0:
                filterPaths.append(path)
            else:
                print("Filtered: " + str(path))
        self.causalPaths = filterPaths
        self.__printPaths()
    
    def __getPathScore(self, path):
        count = 0
        for index in range(len(path) - 1):
            if self.observationGraph[path[index]][path[index+1]] > 0:
                count += self.observationGraph[path[index]][path[index+1]]
        return count

    
    def __printPaths(self):
        print(len(self.causalPaths))
        for path in self.causalPaths:
            print(self.__getLabelledPath(path))
    
    def __getLabelledPath(self, path):
        pathString = ""
        for node in path:
            pathString = pathString + self.componentIdToLabelMap[node] + " -> "
            # pathString = pathString + str(node) + " -> "
        pathString = pathString + str(self.__getPathScore(path))
        return pathString
