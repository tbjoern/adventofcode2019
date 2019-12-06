candidates = []
for i in range(152085,670284):
    digits = [i // 100000, i // 10000, i // 1000, i // 100, i // 10, i]
    digits = [i % 10 for i in digits]
    doubles = set()
    doubles_uniq = set()
    ascending = True
    for a,b in zip(digits, digits[1:]):
        if a == b:
            if a in doubles: 
                if a in doubles_uniq:
                    doubles_uniq.remove(a)
            else:
                doubles_uniq.add(a)
            doubles.add(a)
        if a > b:
            ascending = False
    
    if doubles_uniq and ascending:
        candidates.append(i)
print(len(candidates))


        
