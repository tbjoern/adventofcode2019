wires = [line.strip().split(',') for line in open('input.txt','r').readlines()]

DX = { 'L': -1, 'R': 1, 'U':0, 'D':0}
DY = { 'L': 0, 'R': 0, 'U':1, 'D':-1}
def parse_wire(wire):
    fields = {}
    x = 0
    y = 0
    steps = 0
    for seg in wire:
        d = seg[0]
        assert d in 'LRUD'
        length = int(seg[1:])
        for i in range(length):
            x += DX[d]
            y += DY[d]
            steps += 1
            if (x,y) not in fields:
                fields[(x,y)] = steps
    return fields

a = parse_wire(wires[0])
b = parse_wire(wires[1])

both = a.keys()&b.keys()
dist = [abs(x) + abs(y) for x,y in both]
print(min(dist))
path = [a[p] + b[p] for p in both]
print(min(path))

