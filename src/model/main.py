import sys
sys.path.append('../parser')

from mm import MysteryMachine
from parser.data_struct import Instruction
from parser.node import InputComponents

def mainSolver():
    input = InputComponents()
    input.findInputComponents()
    print(input.components)
    print(input.componentIndexMap)
    for instr in input.instructions:
        print(instr)
    # for node in input.nodes:
    #     print(node)
    used, notUsed = 0, 0
    for observation in input.observationCollection.observations:
        if observation.used:
            used = used + 1
        else:
            # print(observation)
            notUsed = notUsed + 1
    print(used)
    print(notUsed)
    print(len(input.instructions))
    

    # input = ["Apple", "Banana", "Cucumber", "Peach"]
    # instructions = [
    #     Instruction(caller="Apple", callee="Banana"),
    #     Instruction(caller="Cucumber", callee="Peach"),
    #     Instruction(caller="Banana", callee="Cucumber"),
    #     Instruction(caller="Apple", callee="Banana"),
    #     Instruction(caller="Apple", callee="Banana"),
    #     Instruction(caller="Cucumber", callee="Peach")
    # ]
    mysteryMachine = MysteryMachine(input.components, input.instructions)
    mysteryMachine.constructModel()
    print(mysteryMachine.componentMap)
    print(mysteryMachine.causalGraph)
    print(mysteryMachine.observationGraph)
    print("Paths")
    mysteryMachine.EnumeratePaths()

if __name__ == '__main__':
    mainSolver()