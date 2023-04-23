from data_struct import Observation, ObservationCollection
from data_parser import InputParser
from data_struct import Instruction

class ResponseVector:
    def __init__(self, caller, request, response):
        self.caller = caller
        self.request = request
        self.response = response

    def __str__(self):
        return f"ResponseVector(caller={self.caller}, request={self.request}, response={self.response})"

class Node:
    def __init__(self, id, name):
        self.id = id
        self.serviceName = name
        self.responseCollection: ResponseVector = []
        self.childNodes: Node = []
        self.deterministic = True

    def addObservedResponse(self, response: ResponseVector):
        self.responseCollection.append(response)
    
    def checkNodeDeterministic(self):
        n = len(self.responseCollection)
        for resIndex in range(n):
            resVec = self.responseCollection[resIndex]
            for compIndex in range(resIndex + 1, n):
                comVec = self.responseCollection[compIndex]
                if resVec.caller == comVec.caller and resVec.request == comVec.request and resVec.response != comVec.response:
                    self.deterministic = False
                    return

    #################################################################    PRINTING    ############################################################
           
    def __str__(self):
        strOut = "ID: " + str(self.id) + ", Name: " + self.serviceName + ", Deterministic: " + str(self.deterministic)
        for response in self.responseCollection:
            strOut = strOut + "\n" + str(response)
        return strOut
    
class InputComponents:
    FILE_LOCATION = "../trace/logs/trace.json"
    SERVICE_NAME_DELIMITER = "_"
    DEFAULT_REQUEST = "DEFAULT"

    def __init__(self):
        self.components: str = []
        self.nodes: Node = []
        self.componentIndexMap = {}
        self.instructions: Instruction = []
        self.observationCollection: ObservationCollection

    def __loadObservationsFromData(self):
        inputParser = InputParser(file_path=self.FILE_LOCATION)
        self.observationCollection = inputParser.getObservationsFromInput()

    def __createNodeByName(self, nodeName):
        if nodeName not in self.componentIndexMap:
            index = len(self.components)
            self.components.append(nodeName)
            node = Node(index, nodeName)
            self.nodes.append(node)
            self.componentIndexMap[nodeName] = index

    def __addResponseForNode(self, nodeName, callerName, request, response):
        node: Node = self.nodes[self.componentIndexMap[nodeName]]
        node.addObservedResponse(ResponseVector(callerName, request, response))

    def __addInstruction(self, callee, caller):
        instr = Instruction(callee, caller)
        self.instructions.append(instr)
    
    def __processObservation(self, observation: Observation):
        serviceName = observation.requestName.split(self.SERVICE_NAME_DELIMITER)[0]
        callerName = ""
        self.__createNodeByName(serviceName)
        if observation.parentTraceId != "":
            if observation.parentTraceId in self.observationCollection.traceIdToObsIndexMap:
                callerObsv: Observation = self.observationCollection.observations[self.observationCollection.traceIdToObsIndexMap[observation.parentTraceId]]
                callerName = callerObsv.requestName.split(self.SERVICE_NAME_DELIMITER)[0]
                self.__createNodeByName(callerName)
                self.__addInstruction(serviceName, callerName)
        if observation.requestResult != "":
            self.__addResponseForNode(serviceName, callerName, self.DEFAULT_REQUEST, observation.requestResult)

    def __processObservationCollection(self):
        for observation in self.observationCollection.observations:
            self.__processObservation(observation)

    def findInputComponents(self):
        self.__loadObservationsFromData()
        # print(self.observationCollection)
        self.__processObservationCollection()
        for node in self.nodes:
            node.checkNodeDeterministic()
