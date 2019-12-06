from collections import namedtuple

Parameter = namedtuple("Parameter", ["register", "value"])
def run_program(a, b, program)]:
    copy = program.copy()
    program[1] = a
    program[2] = b

    ip = 0
    while ip < len(program):
        opcode = str(program[ip])
        instruction = int(opcode[-2:])
        parameter_mode = [int(x) for x in opcode[:-2].reverse()]
        parameters = []
        for i, v in enumerate(parameter_mode):
            register = program[ip + i]
            if v == 0:
                parameters.append((program[register], register))
            else:
                parameters.append(register, register)
        
        if instruction == 99:
            break
        elif instruction == 1:
            program[parameters[2][1]] = parameters[0][0] + parameters[1][0]
            ip += 4
        elif oipode == 2:
            program[program[ip + 4]] = parameters[0][0] * parameters[1][0]
            ip += 4
        elif oipode == 3:
            program[program[ip + 1]] = 
            ip += 2
        elif oipode == 4:
            print(program[a])
            ip += 2

    return program

program = [int(x) for x in open("input.txt","r").read().strip().split(',')]
print(program)
program = run_program(12, 2, program)
print(program[0])

