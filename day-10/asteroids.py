from math import sqrt,atan2,pi
inp = open('input.txt','r').readlines()

class Vec2:
    def __init__(self, pair, length = None):
        self.x = pair[0]
        self.y = pair[1]
        if length is None:
            self.length = sqrt(self.x**2 + self.y**2)
        else:
            self.length = length
        self.angle = atan2(self.x, self.y)

    def __repr__(self):
        return f"Vec2({self.x},{self.y})"

    def __hash__(self):
        return self.x * 1000 + self.y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vec2((x,y))

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vec2((x,y))

    def __neg__(self):
        return Vec2((-self.x, -self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def normalized(self):
        x = self.x / self.length
        y = self.y / self.length
        return Vec2((x,y), self.length)

def overlap(a , b):
    angle_a = atan2(a.x, a.y)
    angle_b = atan2(b.x, b.y)
    return angle_a == angle_b

asteroids = {}
for i, line in enumerate(inp):
    for j, field in enumerate(line):
        if field == '#':
            asteroids[(j,i)] = 0

for root in asteroids.keys():
    seeable = set()
    root_loc = Vec2(root)
    for asteroid in asteroids.keys():
        asteroid_loc = Vec2(asteroid)
        if asteroid_loc == root_loc:
            continue
        asteroid_vec = asteroid_loc - root_loc
        for maybe_obscured in list(seeable):
            if overlap(asteroid_vec, maybe_obscured):
                if maybe_obscured.length > asteroid_vec.length:
                    seeable.remove(maybe_obscured)
                else:
                    break
        else:
            seeable.add(asteroid_vec)

    asteroids[root] = seeable

asteroid_station = max(asteroids.keys(), key=lambda x: len(asteroids[x]))
asteroid_station_loc = Vec2(asteroid_station)
print(asteroid_station_loc)
print(len(asteroids[asteroid_station]))
destruction_order = sorted(asteroids[asteroid_station], key=lambda x: x.angle)
destruction_order.reverse()
print(destruction_order[199] + asteroid_station_loc)
