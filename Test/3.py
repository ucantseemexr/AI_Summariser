def toolchanger(tools, startIndex, target):
    for i in range(len(tools)):
        if tools[(startIndex + i) % len(tools)] == target or tools[(startIndex - i + len(tools)) % len(tools)] == target:
            return i

tools1 = ['ballendmill', 'facemill', 'keywaycutter', 'slotdrill']
startIndex1 = 1
target1 = 'slotdrill'

print(toolchanger(tools1, startIndex1, target1))


tools2 = ['facemill', 'slotdrill', 'ballendmill', 'ballendmill'] 
startIndex2 = 0
target2 = 'ballendmill'

print(toolchanger(tools2, startIndex2, target2))

tools3 = ['ballendmill', 'ballendmill', 'facemill', 'slotdrill', 'ballendmill', 'ballendmill'] 
startIndex3 = 1
target3 = 'ballendmill'
print(toolchanger(tools3, startIndex3, target3))