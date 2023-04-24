from node import InputComponents, JsonEncoder
import json

def mainSolver():
    input = InputComponents()
    input.findInputComponents()
    print(json.dumps(input.nodeCaches, cls=JsonEncoder, indent=4))

if __name__ == '__main__':
    mainSolver()