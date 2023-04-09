from mm import Instruction
from mm import MysteryMachine

def mainSolver():
    input = ["Apple", "Banana", "Cucumber", "Peach"]
    instructions = [
        Instruction(caller="Apple", callee="Banana"),
        Instruction(caller="Cucumber", callee="Peach"),
        Instruction(caller="Banana", callee="Cucumber"),
        Instruction(caller="Apple", callee="Banana"),
        Instruction(caller="Apple", callee="Banana"),
        Instruction(caller="Cucumber", callee="Peach")
    ]
    mysteryMachine = MysteryMachine(input, instructions)
    mysteryMachine.constructModel()
    print(mysteryMachine.componentMap)
    print(mysteryMachine.causalGraph)
    print(mysteryMachine.observationGraph)
    print("Paths")
    mysteryMachine.EnumeratePaths()

if __name__ == '__main__':
    mainSolver()