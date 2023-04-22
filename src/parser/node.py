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
    def __init__(self, name):
        self.serviceName = name
        self.responseCollection: ResponseVector = []

    def addObservedResponse(self, response: ResponseVector):
        self.responseCollection.append(response)

    def __str__(self):
        strOut = self.serviceName
        for response in self.responseCollection:
            strOut = strOut + "\n" + str(response)
        return strOut
    
class InputComponents:
    FILE_LOCATION = "../trace/logs/trace_full.json"
    SERVICE_NAME_DELIMITER = "_"
    TARGET_NAME_DELIMITER = "/"
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
            node = Node(nodeName)
            self.nodes.append(node)
            self.componentIndexMap[nodeName] = index

    def __addResponseForNode(self, nodeName, callerName, request, response):
        node: Node = self.nodes[self.componentIndexMap[nodeName]]
        node.addObservedResponse(ResponseVector(callerName, request, response))

    def __addInstruction(self, callee, caller):
        instr = Instruction(callee, caller)
        self.instructions.append(instr)
    
    def __processObservation(self, observation: Observation):
        if observation.parentSpanId == "":
            return
        if observation.parentSpanId in self.observationCollection.spanIdToObsIndexMap:
            callerObsv: Observation = self.observationCollection.observations[self.observationCollection.spanIdToObsIndexMap[observation.parentSpanId]]
            if observation.requestTarget != "" and self.SERVICE_NAME_DELIMITER in callerObsv.requestName:
                callerName = callerObsv.requestName.split(self.SERVICE_NAME_DELIMITER)[0]
                targetName = observation.requestTarget.split(self.TARGET_NAME_DELIMITER)[-1]
                if targetName == "":
                    targetName = "/"
                self.__createNodeByName(callerName)
                self.__createNodeByName(targetName)
                self.__addResponseForNode(targetName, callerName, self.DEFAULT_REQUEST, callerObsv.requestResult)
                self.__addInstruction(targetName, callerName)
                callerObsv.used = True
                observation.used = True
        else:
            print(observation.parentSpanId + " NOT FOUND :(")

    def __processObservationCollection(self):
        for observation in self.observationCollection.observations:
            self.__processObservation(observation)

    def findInputComponents(self):
        self.__loadObservationsFromData()
        # print(self.observationCollection)
        self.__processObservationCollection()
