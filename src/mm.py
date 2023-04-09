import numpy as np

class Instruction:
        def __init__(self, callee, caller):
            self.callee = callee
            self.caller = caller

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
            for j in range(n):
                if self.causalGraph[i][j] == 1:
                    nodeAdded[i] = 1
                    self.__explorePaths([i], j, n, nodeAdded)
            nodeAdded[i] = 0
        
        self.__printPaths()

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
    
    def __printPaths(self):
        for path in self.causalPaths:
            print(self.__getLabelledPath(path))
    
    def __getLabelledPath(self, path):
        pathString = ""
        for node in path:
            pathString = pathString + self.componentIdToLabelMap[node] + " -> "
        return pathString[:-3]
