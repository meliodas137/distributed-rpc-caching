class Instruction:
    def __init__(self, callee, caller):
        self.callee = callee
        self.caller = caller

    #################################################################    PRINTING    ############################################################
    
    def __str__(self):
        return f"Instruction({self.caller} --> {self.callee})"

class Observation:
    def __init__(self, id, traceId, spanId, parentTraceId, requestName, requestRes):
        self.id = id
        self.traceId = traceId
        self.spanId = spanId
        self.parentTraceId = parentTraceId
        self.requestName = requestName
        self.requestResult = requestRes

    #################################################################    PRINTING    ############################################################

    def __str__(self):
        return f"Observation(id={self.id}, traceId={self.traceId}, spanId={self.spanId}, parentTraceId={self.parentTraceId}, requestName={self.requestName}, requestOutput={self.requestResult})"
    
class ObservationCollection:
    def __init__(self):
        self.observations: Observation = []
        self.traceIdToObsIndexMap = {}

    def addObservation(self, observation: Observation):
        self.observations.append(observation)
        self.traceIdToObsIndexMap[observation.traceId] = observation.id

    #################################################################    PRINTING    ############################################################

    def __str__(self):
        strOut = "Observations: " + str(len(self.observations))
        for obs in self.observations:
            strOut = strOut + "\n" + str(obs)
        return strOut