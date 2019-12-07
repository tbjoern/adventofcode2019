from collections import deque
from itertools import permutations

class Parameter:
    def __init__(self, addr, program):
        self.addr = addr
        self.program = program

    def _get_value(self):
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

class IntcodeProgram:
    def __init__(self, program):
        self.program = program
        self.registers = self.program.copy()
        self.instruction_counter = 0
        self.outputs = []
        self.running = False
        self.halted = False

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
        self.registers = self.program.copy()
        self.instruction_counter = 0
        self.outputs = []
        self.halted = False

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
}

program_code = [int(x) for x in open("program.txt","r").read().strip().split(',')]
#program.run()
def run_amplifier_stack(amp_settings, program_code):
    output = 0
    amps = [IntcodeProgram(program_code) for _ in amp_settings]
    connectors = [ProgramConnector() for _ in amp_settings]
    prev_connector = connectors[4]
    for amp, amp_setting, connector in zip(amps, amp_settings, connectors):
        amp.output_sink = connector
        amp.input_gen = prev_connector
        prev_connector.append(amp_setting)
        prev_connector = connector
        amp.pause_on_output = True

    connectors[4].append(0)

    while True:
        for amp in amps:
            amp.run()
            halted = amp.halted
        if halted:
            break
    return amps[4].outputs[-1]

part_1_settings = permutations([0,1,2,3,4])
signals = [run_amplifier_stack(amp_settings, program_code) for amp_settings in part_1_settings]
print(max(signals))


part_2_settings = permutations([5,6,7,8,9])
signals = [run_amplifier_stack(amp_settings, program_code) for amp_settings in part_2_settings]
print(max(signals))

