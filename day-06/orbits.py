from collections import deque
class Planet:
    def __init__(self, name, parent=None):
        self.parent = parent
        self.name = name
        self.satelites = []

    def neighbours(self):
        if self.parent is None:
            return self.satelites
        return self.satelites + [self.parent]

    def add(self, satelite):
        self.satelites.append(satelite)
        satelite.parent = self

    def orbit_count(self):
        aggregate = [s.orbit_count() for s in self.satelites]
        direct_satelites = len(self.satelites)
        indirect_satelites = sum(x[0] for x in aggregate)
        total_orbits = sum(x[1] for x in aggregate) + direct_satelites + indirect_satelites
        return (direct_satelites + indirect_satelites, total_orbits)

class PlanetMap:
    def __init__(self):
        self.map = { 'COM': Planet('COM') }

    def __repr__(self):
        return "\n".join(x for x in self.map.keys())

    def create(self, body):
        if not body in self.map:
            self.map[body] = Planet(body)

    def add(self, body, satelite):
        self.create(body)
        self.create(satelite)
        self.map[body].add(self.map[satelite])

planet_map = PlanetMap()
for line in open('input.txt', 'r'):
    body, satelite = line.strip().split(')')
    planet_map.add(body, satelite)

print(planet_map.map['COM'].orbit_count())

search = deque()
visited = set()
search.append((planet_map.map['YOU'], -1))
while deque:
    planet, steps = search.popleft()
    print(planet.name)
    visited.add(planet.name)
    for neighbour in planet.neighbours():
        if neighbour.name == 'SAN':
            print(steps)
            exit()
        if not neighbour.name in visited:
            search.append((neighbour, steps + 1))



