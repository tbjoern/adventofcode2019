from collections import namedtuple

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

