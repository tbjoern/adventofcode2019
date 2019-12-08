width = 25
height = 6
pixel_count = width*height

data = open('input.txt','r').read().strip()
data_iter = iter(data)

counts = []
layer_count = len(data) // pixel_count
for i in range(layer_count):
    digits0 = 0
    digits1 = 0
    digits2 = 0
    for j in range(pixel_count):
        digit = next(data_iter)
        digits0 += int(digit == '0')
        digits1 += int(digit == '1')
        digits2 += int(digit == '2') 
    counts.append((digits0, digits1 * digits2))

counts.sort(key=lambda x: x[0])
print(counts[0])

image = ['2' for _ in range(pixel_count)]
data_iter = iter(data)
for i in range(layer_count):
    for j in range(pixel_count):
        d = next(data_iter)
        if image[j] == '2':
            image[j] = d

line = []
pixel_map = {
        '0': ' ',
        '1': '#',
}
for i,p in enumerate(image):
    line.append(pixel_map[p])
    if i % width == 24:
        print("".join(line))
        line = []

