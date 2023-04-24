from data_struct import Observation, ObservationCollection
from data_parser import InputParser
from data_struct import Instruction
from typing import Dict, List
import json

class ResponseVector:
    def __init__(self, input, output):
        self.deterministic = True
        self.input = input
        self.output = output

    
class ResponseTable:
    def __init__(self):
        self.responses: List[ResponseVector] = []

    def addResponse(self, response: ResponseVector):
        self.responses.append(response)


class Node:
    def __init__(self, id, name):
        self.id = id
        self.serviceName = name
        self.forwardingTable: Dict[str, ResponseTable] = {}

    def addObservedResponse(self, serviceToCall: str, response: ResponseVector):
        if serviceToCall not in self.forwardingTable:
            responses = ResponseTable()
            responses.addResponse(response)
            self.forwardingTable[serviceToCall] = responses
        else:
            for observedResponse in self.forwardingTable[serviceToCall].responses:
                if observedResponse.input == response.input:
                    if observedResponse.output == response.output:
                        return
                    else:
                        observedResponse.deterministic = False
                        return
            self.forwardingTable[serviceToCall].responses.append(response)


class NodeCaches:
    def __init__(self, nodes):
        self.services = nodes


class InputComponents:
    INPUT_FILE_LOCATION = "../trace/logs/trace_full.json"
    SERVICE_NAME_DELIMITER = "_"
    DEFAULT_REQUEST = "DEFAULT"

    def __init__(self):
        self.components: str = []
        self.nodes: Node = []
        self.componentIndexMap = {}
        self.instructions: Instruction = []
        self.observationCollection: ObservationCollection
        self.nodeCaches: NodeCaches = None

    def __loadObservationsFromData(self):
        inputParser = InputParser(file_path=self.INPUT_FILE_LOCATION)
        self.observationCollection = inputParser.getObservationsFromInput()

    def __createNodeByName(self, nodeName):
        if nodeName not in self.componentIndexMap:
            index = len(self.components)
            self.components.append(nodeName)
            node = Node(index, nodeName)
            self.nodes.append(node)
            self.componentIndexMap[nodeName] = index

    def __addResponseForNode(self, nodeName, calledService, input, output):
        node: Node = self.nodes[self.componentIndexMap[nodeName]]
        node.addObservedResponse(calledService, ResponseVector(input, output))
    
    def __processObservation(self, observation: Observation):
        serviceName = observation.serviceName.split(self.SERVICE_NAME_DELIMITER)[0]
        parentName = ""
        self.__createNodeByName(serviceName)
        if observation.parentTraceId != "":
            if observation.parentTraceId in self.observationCollection.traceIdToObsIndexMap:
                parentObsv: Observation = self.observationCollection.observations[self.observationCollection.traceIdToObsIndexMap[observation.parentTraceId]]
                parentName = parentObsv.serviceName.split(self.SERVICE_NAME_DELIMITER)[0]
                self.__createNodeByName(parentName)
                self.__addResponseForNode(parentName, serviceName, observation.input, observation.output)

    def __processObservationCollection(self):
        for observation in self.observationCollection.observations:
            self.__processObservation(observation)

    def findInputComponents(self):
        self.__loadObservationsFromData()
        self.__processObservationCollection()
        self.nodeCaches = NodeCaches(self.nodes)


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Node):
            return {
                'id': obj.id,
                'serviceName': obj.serviceName,
                'forwardingTable': obj.forwardingTable
            }
        if isinstance(obj, ResponseTable):
            return {
                'responses': obj.responses
            }
        if isinstance(obj, ResponseVector):
            return {
                "input": obj.input,
                "output": obj.output,
                "deterministic": obj.deterministic
            }
        if isinstance(obj, NodeCaches):
            return {
                "services": obj.services
            }
        return super(JsonEncoder, self).default(obj)