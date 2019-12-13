from time import sleep
import sys
from collections import deque
from itertools import permutations
import keyboard
import curses

class Parameter:
    def __init__(self, addr, program):
        self.addr = addr
        self.program = program

    def __repr__(self):
        return f"{self._get_value()}"

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
        self.verbose = False

    def output(self, value):
        if self.output_sink is not None:
            self.output_sink.append(value)
        self.outputs.append(value)
        if self.verbose:
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

    def print_instructions(self):
        counter = 0
        while counter < len(self.registers): 
            instruction = Instruction.from_program(self)
            sys.stdout.write(f"{counter}: ")
            print(str(instruction))
            counter += type(instruction).parameter_count()



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

class ScreenDrawer:
    def __init__(self, window):
        self.window = window
        self.values = []
        self.tile_map = { 0: ' ', 1: 'X', 2: 'B', 3: '-', 4: 'o' } 

    def append(self, value):
        self.values.append(value)
        if len(self.values) == 3:
            x,y,tile = self.values
            if x != -1:
                self.window.addstr(y,x, self.tile_map[tile])
            else:
                self.window.addstr(29, 0, str(tile))
            self.values = []

def hack_paddle():
    program = IntcodeProgram([int(x) for x in open("input.txt","r").read().strip().split(',')])
    # for register, content in enumerate(program.program):
        # if content == 3:
            # print(register)
    program.print_instructions()

def main(window):
    window.nodelay(False)
    curses.curs_set(0) # hide cursor
    program = IntcodeProgram([int(x) for x in open("input.txt","r").read().strip().split(',')])
    program.run()
    tiles = {}
    for i in range(0, len(program.outputs), 3):
        x,y,tile = (program.outputs[i], program.outputs[i+1], program.outputs[i+2])
        tiles[(x,y)] = tile

    block_count = len([tile for tile in tiles.values() if tile == 2])
    window.addstr(0,0,f"{block_count}")
    x_dim = max(tile[0] for tile in tiles.keys()) 
    y_dim = max(tile[1] for tile in tiles.keys())
    window.addstr(1,0,f"{x_dim} x {y_dim}")
    window.refresh()
    sleep(2)

    def keyboard_input():
        while True:
            window.refresh()
            sleep(0.005)
            key = window.getch()
            window.addstr(28, 0, f"key pressed: {key}")
            if key == 97 or key == 970:
                yield -1
            elif key == 100:
                yield 1
            else:
                yield 0

    def hack_input():
        paddle_loc = 1584
        while True:
            window.refresh()
            sleep(0.1)
            key = window.getch()
            window.addstr(28, 0, f"key pressed: {key}")
            if key == 97 or key == 970:
                paddle_loc -= 1
            elif key == 100:
                paddle_loc += 1
            program.registers[paddle_loc - 2] = 3
            program.registers[paddle_loc - 1] = 3
            program.registers[paddle_loc] = 3
            program.registers[paddle_loc + 1] = 3
            program.registers[paddle_loc + 2] = 3
            yield 0


    program.input_gen = keyboard_input()
    program.output_sink = ScreenDrawer(window)

    while True:
        window.clear()
        
        program.reset()
        program.registers[0] = 2
        paddle_loc = 1584
        for i in range(1564, 1604):
            program.registers[i] = 3


        window.nodelay(True)
        program.run()
        window.nodelay(False)

        window.addstr(30,0,"Game Over")
        window.refresh()
        window.addstr(31,0,"Press any key to retry")
        window.getch()

curses.wrapper(main)
#hack_paddle()
