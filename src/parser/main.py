from node import InputComponents, JsonEncoder
import json

def mainSolver():
    input = InputComponents()
    input.findInputComponents()
    # print(json.dumps(input.nodeCaches, cls=JsonEncoder, indent=4))
    with open("../trace/cacheInfo.json", "w") as f:
        json.dump(input.nodeCaches, f, cls=JsonEncoder)
    input.printNodeRpcCountTable()
    

if __name__ == '__main__':
    mainSolver()