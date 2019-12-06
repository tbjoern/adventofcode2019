from collections import namedtuple

class Parameter:
    def __init__(self, addr, program):
        self.addr = addr
        self.program = program

    def _get_value(self):
        return program.registers[self.addr]

    def _set_value(self, v):
        program.registers[self.addr] = v

    v = property(_get_value, _set_value)

class Instruction:
    def execute():
        pass

    @classmethod
    def from_program(cls, program):
        _, opcode = next(program)
        instruction_type = opcode % 100
        parameter_modes = opcode // 100
        instruction_cls = INSTRUCTION_MAP[instruction_type]
        parameters = []
        for i in range(instruction_cls.parameter_count()):
            register_addr, register_content = next(program)
            mode = parameter_modes % 10
            parameter_modes = parameter_modes // 10
            if mode == 0:
                parameters.append(Parameter(register_content, program))
            elif mode == 1:
                parameters.append(Parameter(register_addr, program))
            else:
                raise ValueError("Unkown parameter mode")
        return instruction_cls(*parameters)
            

class Add(Instruction):
    def __init__(self, a, b, dest):
        self.a = a
        self.b = b
        self.dest = dest

    def __repr__(self):
        return f"Add {self.a} {self.b} {self.dest}"

    def execute(self, program):
        self.dest.v = self.a.v + self.b.v

    @classmethod
    def parameter_count(cls):
        return 3

class Multiply(Instruction):
    def __init__(self, a, b, dest):
        self.a = a
        self.b = b
        self.dest = dest

    def __repr__(self):
        return f"Multiply {self.a} {self.b} {self.dest}"

    def execute(self, program):
        self.dest.v = self.a.v * self.b.v

    @classmethod
    def parameter_count(cls):
        return 3

class Input(Instruction):
    def __init__(self, register):
        self.register = register

    def __repr__(self):
        return f"Input {self.register}"

    def execute(self, program):
        value = int(input("Gimme a value: "))
        self.register.v = value

    @classmethod
    def parameter_count(cls):
        return 1

class Output(Instruction):
    def __init__(self, register):
        self.register = register

    def __repr__(self):
        return f"Output {self.register}"

    def execute(self, program):
        print(self.register.v)
    
    @classmethod
    def parameter_count(cls):
        return 1

class Halt(Instruction):
    def execute(self, program):
        program.halt()

    def __repr__(self):
        return f"Halt"

    @classmethod
    def parameter_count(cls):
        return 0

class JumpIfTrue(Instruction):
    def __init__(self, test, ip):
        self.test = test
        self.ip = ip

    def __repr__(self):
        return f"JumpIfTrue {self.test} {self.ip}"

    def execute(self, program):
        if self.test.v != 0:
            program.instruction_counter = self.ip.v
            
    @classmethod
    def parameter_count(cls):
        return 2

class JumpIfFalse(Instruction):
    def __init__(self, test, ip):
        self.test = test
        self.ip = ip

    def __repr__(self):
        return f"JumpIfFalse {self.test} {self.ip}"

    def execute(self, program):
        if self.test.v == 0:
            program.instruction_counter = self.ip.v
            
    @classmethod
    def parameter_count(cls):
        return 2

class LessThan(Instruction):
    def __init__(self, a, b, dest):
        self.a = a
        self.b = b
        self.dest = dest

    def __repr__(self):
        return f"LessThan {self.a} {self.b} {self.dest}"

    def execute(self, program):
        self.dest.v = int(self.a.v < self.b.v)

    @classmethod
    def parameter_count(cls):
        return 3

class Equal(Instruction):
    def __init__(self, a, b, dest):
        self.a = a
        self.b = b
        self.dest = dest

    def __repr__(self):
        return f"Equal {self.a} {self.b} {self.dest}"

    def execute(self, program):
        self.dest.v = int(self.a.v == self.b.v)

    @classmethod
    def parameter_count(cls):
        return 3

class IntcodeProgram:
    def __init__(self, program):
        self.program = program
        self.registers = None
        self.instruction_counter = 0
        self.running = False

    def __next__(self):
        ret_val = (self.instruction_counter, self.registers[self.instruction_counter])
        self.instruction_counter += 1
        return ret_val

    def halt(self):
        self.running = False

    def run(self):
        self.running = True
        self.registers = self.program.copy()
        self.instruction_counter = 0
        while self.instruction_counter < len(self.registers) and self.running:
            instruction = Instruction.from_program(self)
            instruction.execute(self)

INSTRUCTION_MAP = {
        99: Halt,
        1: Add,
        2: Multiply,
        3: Input,
        4: Output,
        5: JumpIfTrue,
        6: JumpIfFalse,
        7: LessThan,
        8: Equal,
}

program = IntcodeProgram([int(x) for x in open("input.txt","r").read().strip().split(',')])
program.run()

