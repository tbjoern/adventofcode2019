import math
recipes_raw = open('input.txt','r').readlines()
recipes = {}

class Chemical:
    def __init__(self, count, name):
        self.count = count
        self.name = name

    def __repr__(self):
        return f"{self.count} {self.name}"

    def __str__(self):
        return repr(self)

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def from_string(cls, string):
        count, name = string.split()
        count = int(count.strip())
        name = name.strip()
        return cls(count, name)

for line in recipes_raw:
    ingredients, result = line.strip().split('=>')
    result = Chemical.from_string(result)
    ingredients = ingredients.split(',')
    ingredients = [
            Chemical.from_string(chemical_str)
            for chemical_str in ingredients
    ]
    recipes[result.name] = (result.count, ingredients)

# for chemical, ingredients in recipes.items():
    # print(f"{','.join(str(i) for i in ingredients)} => {chemical}")

ore = 0
fuel = 0
while ore + 654909 < 1000000000000:
    fuel += 1
    target_chemicals = { "FUEL": 1 }
    done = False

    while not done:
        tmp = target_chemicals.copy()
        done = True
        for name, count in tmp.items():
            if count <= 0:
                continue
            done = False
            recipe_yield, ingredients = recipes[name]
            recipe_count = math.ceil(count / recipe_yield)
            for ingredient in ingredients:
                if ingredient.name == "ORE":
                    ore += ingredient.count * recipe_count
                    continue
                if ingredient.name not in target_chemicals:
                    target_chemicals[ingredient.name] = 0
                target_chemicals[ingredient.name] += ingredient.count * recipe_count
            target_chemicals[name] -= recipe_yield * recipe_count

print(ore)
print(fuel)

