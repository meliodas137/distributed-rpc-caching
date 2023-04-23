class Instruction:
    def __init__(self, callee, caller):
        self.callee = callee
        self.caller = caller

    #################################################################    PRINTING    ############################################################
    
    def __str__(self):
        return f"Instruction({self.caller} --> {self.callee})"

class Observation:
    def __init__(self, id, traceId, spanId, parentSpanId, requestName, requestTarget, requestRes):
        self.id = id
        self.traceId = traceId
        self.spanId = spanId
        self.parentSpanId = parentSpanId
        self.requestName = requestName
        self.requestTarget = requestTarget
        self.requestResult = requestRes
        self.used = False

    #################################################################    PRINTING    ############################################################

    def __str__(self):
        return f"Observation(id={self.id}, traceId={self.traceId}, spanId={self.spanId}, parentSpanId={self.parentSpanId}, requestName={self.requestName}, requestTarget={self.requestTarget}, requestOutput={self.requestResult})"
    
class ObservationCollection:
    def __init__(self):
        self.observations: Observation = []
        self.spanIdToObsIndexMap = {}

    def addObservation(self, observation: Observation):
        self.observations.append(observation)
        self.spanIdToObsIndexMap[observation.spanId] = observation.id

    #################################################################    PRINTING    ############################################################

    def __str__(self):
        strOut = "Observations: " + str(len(self.observations))
        for obs in self.observations:
            strOut = strOut + "\n" + str(obs)
        return strOut