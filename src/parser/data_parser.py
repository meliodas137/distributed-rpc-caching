import json
from data_struct import Observation, ObservationCollection

class InputParser:

    JSON_KEY_RESOURCE_SPANS = "resourceSpans"
    JSON_KEY_SCOPE_SPANS = "scopeSpans"
    JSON_KEY_SPANS = "spans"
    JSON_KEY_ZERO = 0
    JSON_KEY_TRACE_ID = "traceId"
    JSON_KEY_SPAN_ID = "spanId"
    JSON_KEY_PARENT_TRACE_ID = "service.parentId"
    JSON_KEY_NAME = "name"
    JSON_KEY_ATTRIBUTES = "attributes"
    JSON_KEY_KEY = "key"
    JSON_KEY_VALUE = "value"
    JSON_KEY_STRING_VALUE = "stringValue"
    JSON_KEY_INT_VALUE = "intValue"

    HTTP_TARGET = "http.target"
    SERVICE_INPUT = "service.input"
    SERVICE_OUTPUT = "service.output"

    def __init__(self, file_path):
        self.filePath = file_path

    def __readNextLine(self):
        with open(self.filePath , 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                yield line.strip()

    def getObservationsFromInput(self):
        observationCollection = ObservationCollection()
        id = 0
        for line in self.__readNextLine():
            jsonData = json.loads(line)
            spanData = jsonData[self.JSON_KEY_RESOURCE_SPANS][self.JSON_KEY_ZERO][self.JSON_KEY_SCOPE_SPANS][self.JSON_KEY_ZERO][self.JSON_KEY_SPANS][self.JSON_KEY_ZERO]
            traceId = spanData[self.JSON_KEY_TRACE_ID]
            spanId = spanData[self.JSON_KEY_SPAN_ID]
            reqName = spanData[self.JSON_KEY_NAME]
            parentTraceId, input, reqOutput = "", "", ""
            attributesData = spanData[self.JSON_KEY_ATTRIBUTES]
            if attributesData:
                for attribute in attributesData:
                    key = attribute[self.JSON_KEY_KEY]
                    try:
                        value = attribute[self.JSON_KEY_VALUE][self.JSON_KEY_STRING_VALUE]
                    except Exception:
                        value = attribute[self.JSON_KEY_VALUE][self.JSON_KEY_INT_VALUE]
                    if key == self.SERVICE_OUTPUT:
                        reqOutput = value
                    if key == self.JSON_KEY_PARENT_TRACE_ID:
                        parentTraceId = value
                    if key == self.SERVICE_INPUT:
                        input = value
            obs = Observation(id, traceId, spanId, parentTraceId, reqName, input, reqOutput)
            observationCollection.addObservation(obs)
            id = id + 1
        return observationCollection
