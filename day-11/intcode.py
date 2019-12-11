from collections import deque
from itertools import permutations

class Parameter:
    def __init__(self, addr, program):
        self.addr = addr
        self.program = program

    def _get_value(self):
        if self.addr not in self.program.registers:
            self.program.registers[self.addr] = 0
        return self.program.registers[self.addr]

    def _set_value(self, v):
        self.program.registers[self.addr] = v

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
            elif mode == 2:
                parameters.append(Parameter(program.relative_base + register_content, program))
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
        if program.input_gen is None:
            value = int(input("Gimme a value: "))
        else:
            value = next(program.input_gen)
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
        program.output(self.register.v)
    
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

class RelativeBase(Instruction):
    def __init__(self, base):
        self.base = base

    def __repr__(self):
        return f"RelativeBase {self.base}"
    
    def execute(self, program):
        program.relative_base += self.base.v

    @classmethod
    def parameter_count(cls):
        return 1


class IntcodeProgram:
    def __init__(self, program):
        self.program = program
        self.reset()

        self.input_gen = None
        self.output_sink = None
        self.pause_on_output = False

    def output(self, value):
        if self.output_sink is not None:
            self.output_sink.append(value)
        self.outputs.append(value)
        print(value)
        if self.pause_on_output:
            self.running = False

    def __next__(self):
        ret_val = (self.instruction_counter, self.registers[self.instruction_counter])
        self.instruction_counter += 1
        return ret_val

    def halt(self):
        self.running = False
        self.halted = True

    def reset(self):
        self.registers = {i:v for i,v in enumerate(self.program.copy())}
        self.instruction_counter = 0
        self.relative_base = 0
        self.outputs = []
        self.halted = False
        self.running = False

    def run(self):
        self.running = True
        while self.instruction_counter < len(self.registers) and self.running:
            instruction = Instruction.from_program(self)
            instruction.execute(self)

class ProgramConnector:
    def __init__(self):
        self.values = deque()

    def append(self, value):
        self.values.append(value)

    def __next__(self):
        return self.values.popleft()

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
        9: RelativeBase,
}

program = IntcodeProgram([int(x) for x in open("input.txt","r").read().strip().split(',')])
program.pause_on_output = True
panels = { (0,0) : 1}
x = 0
y = 0
facing = 0
def pos_gen():
    while True:
        if (x,y) not in panels:
            panels[(x,y)] = 0
        yield panels[(x,y)]
program.input_gen = pos_gen()
while not program.halted:
    program.run()
    program.run()
    try:
        color, rotation = program.outputs
    except:
        color = program.outputs[0]
    program.outputs = []
    panels[(x,y)] = color
    if rotation == 1:
        facing += 1
    else:
        facing -= 1
    facing = facing % 4
    if facing == 0:
        y += 1
    elif facing == 1:
        x += 1
    elif facing == 2:
        y -= 1
    elif facing == 3:
        x -= 1

print(len(panels))

max_x = max(panels.keys(), key=lambda p: p[0])[0]
max_y = max(panels.keys(), key=lambda p: p[1])[1]
min_x = min(panels.keys(), key=lambda p: p[0])[0]
min_y = min(panels.keys(), key=lambda p: p[1])[1]
print(abs(max_x - min_x))
print(abs(max_y - min_y))
for j in range(max_y, min_y - 1, -1):
    line = []
    for i in range(min_x, max_x + 1, 1):
        value = panels.get((i,j), 0)
        if value == 1:
            pixel = '#'
        else:
            pixel = ' '
        line.append(pixel)
    print("".join(line))


