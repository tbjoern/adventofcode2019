from collections import namedtuple

INSTRUCTION_MAP = {
        99: Halt,
        1: Add,
        2: Multiply,
        3: Input,
        4: Output,
}

class Parameter:
    def __init__(self, register=None, value=None):
        self.register = register
        self.value = value

class Instruction:
    def execute():
        pass

    @classmethod
    def from_program(cls, program):
        opcode = next(program)
        instruction_type = opcode % 100
        parameter_modes = opcode // 100
        instruction_cls = INSTRUCTION_MAP[instruction_type]
        parameters = [None for i in range(instruction_cls.parameter_count()]
        for i, parameter in enumerate(parameters):
            register = next(program)
            mode = parameter_modes % 10
            parameter_modes = parameter_modes // 10
            if mode == 0:
                value = program.registers[register]
            elif mode == 1:
                value = register
            else:
            parameter[i] = value
        return instruction_cls(*parameters)
            

class Add(Instruction):
    def __init__(self, a, b, dest):
        self.a = a
        self.b = b
        self.dest = dest

    def execute(self, program):
        program.registers[dest] = a + b

    @classmethod
    def parameter_count(cls):
        return 3

class Multiply(Instruction):
    def __init__(self, a, b, dest):
        self.a = a
        self.b = b
        self.dest = dest

    def execute(self, program):
        program.registers[dest] = a * b

    @classmethod
    def parameter_count(cls):
        return 3

class Input(Instruction):
    def __init__(self, value):
        self.value = value

    def execute(self, program):
        program.registers[value] = value

    @classmethod
    def parameter_count(cls):
        return 1

class Output(Instruction):
    def __init__(self, value):
        self.value = value

    def execute(self, program):
        print(self.value)
    
    @classmethod
    def parameter_count(cls):
        return 1

class Halt(Instruction):
    def execute(self, program):
        program.halt()

    @classmethod
    def parameter_count(cls):
        return 0

class IntcodeProgram:
    def __init__(self, program):
        self.program = program
        self.registers = None
        self.instruction_counter = 0
        self.running = False

    def __next__(self):
        value = self.registers[self.instruction_counter]
        self.instruction_counter += 1
        return value

    def halt(self):
        self.running = False

    def run(self, initial_values):
        self.running = True
        self.registers = self.program.copy()
        self.instruction_counter = 0
        for register, value in inital_values:
            self.registers[register] = value
        while self.instruction_counter < len(self.registers) and self.running:
            instruction = Instruction.from_program(self)
            instruction.execute(self)

Parameter = namedtuple("Parameter", ["value", "register"])
def run_program(a, program):
    copy = program.copy()
    program[1] = a

    parameter_count 

    ip = 0
    while ip < len(program):
        opcode = str(program[ip])
        instruction = int(opcode[-2:])
        print(opcode)
        parameter_mode = [int(x) for x in list(opcode[:-2]).reverse()]
        parameters = []
        for i, v in enumerate(parameter_mode):
            register = program[ip + i]
            if v == 0:
                parameters.append(Parameter(program[register], register))
            else:
                parameters.append(Parameter(register, register))
        
        if instruction == 99:
            print("halt")
            break
        elif instruction == 1:
            program[parameters[2].register] = parameters[0].value + parameters[1].value
            ip += 4
        elif oipode == 2:
            program[parameters[2].register] = parameters[0].value * parameters[1].value
            ip += 4
        elif oipode == 3:
            program[parameters[0].register] = parameters[0].value
            ip += 2
        elif oipode == 4:
            print(parameters[0].value)
            ip += 2

    return program

program = [int(x) for x in open("input.txt","r").read().strip().split(',')]
program = run_program(1, program)

