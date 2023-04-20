import sys
sys.path.append('../parser')

from mm import MysteryMachine
from graph import Graph, NodeGraph
from parser.data_struct import Instruction
from parser.node import InputComponents, Node

def generateNodes(components):
    nodes, mark = [], ["Apple"]
    c = 0
    for component in components:
        node = Node(c, component)
        if component in mark:
            node.deterministic = False
        nodes.append(node)
        c = c+1
    return nodes

def mainSolver():
    input = InputComponents()
    # input.findInputComponents()
    # print(input.components)
    # print(input.componentIndexMap)
    # for instr in input.instructions:
    #     print(instr)
    # for node in input.nodes:
    #     print(node)
    # used, notUsed = 0, 0
    # for observation in input.observationCollection.observations:
    #     if observation.used:
    #         used = used + 1
    #     else:
    #         print(observation)
    #         notUsed = notUsed + 1
    # print(used)
    # print(notUsed)
    # print(len(input.instructions))
    

    input.components = ["Eatables", "Meat", "Fruit", "Apple", "Veggies", "Brocolli"]
    input.instructions = [
        Instruction(caller="Eatables", callee="Meat"),
        Instruction(caller="Eatables", callee="Fruit"),
        Instruction(caller="Eatables", callee="Veggies"),
        Instruction(caller="Eatables", callee="Meat"),
        Instruction(caller="Eatables", callee="Fruit"),
        Instruction(caller="Fruit", callee="Apple"),
        Instruction(caller="Fruit", callee="Apple"),
        Instruction(caller="Veggies", callee="Brocolli"),
        Instruction(caller="Veggies", callee="Brocolli"),
        Instruction(caller="Eatables", callee="Meat")
    ]
    # input.components = ["a", "b", "c"]
    # input.instructions = [
    #     Instruction(caller="a", callee="b"),
    #     Instruction(caller="a", callee="c"),
    #     Instruction(caller="a", callee="b"),
    #     Instruction(caller="a", callee="b"),
    #     Instruction(caller="a", callee="c"),
    #     Instruction(caller="a", callee="c")
    # ]
    input.nodes = generateNodes(input.components)
    mysteryMachine = MysteryMachine(input.components, input.instructions)
    mysteryMachine.constructModel()
    print(mysteryMachine.componentMap)
    print(mysteryMachine.causalGraph)
    print(mysteryMachine.observationGraph)
    print("All Models")
    mysteryMachine.EnumeratePaths()
    print("Chosen Model")
    graph: Graph = mysteryMachine.chooseGraphModel()
    print(graph)
    print(graph.printLabelledGraph(input.components))
    model = NodeGraph(input.nodes, graph)
    print(model)
    sets = mysteryMachine.generateAllSets([1,2,3])
    print(sets)
    print(sets[7])

if __name__ == '__main__':
    mainSolver()