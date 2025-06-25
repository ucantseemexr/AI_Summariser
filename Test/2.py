def getMaxUnits(boxes, unitsPerBox, truckSize):
    for i in range(len(unitsPerBox)):
        for j in range(len(unitsPerBox) - i - 1):
            if unitsPerBox[j] <= unitsPerBox[j + 1]:
                temp = unitsPerBox[j]
                unitsPerBox[j] = unitsPerBox[j + 1]
                unitsPerBox[j + 1] = temp
                
                boxes[j], boxes[j + 1] = boxes[j + 1], boxes[j]
                
    print(boxes)
    print(unitsPerBox)
    
    total = 0
    for i in range(truckSize):
        for j in range(len(unitsPerBox)):
            if boxes[j] > 0:
                total += unitsPerBox[j]
                boxes[j] -= 1
                break
            
    return total

boxes1 = [1, 2, 3]
unitsPerBox1 = [3, 2, 1]
truckSize1 = 3
print(getMaxUnits(boxes1, unitsPerBox1, truckSize1)) 

boxes2 = [3, 1, 6]
unitsPerBox2 = [2, 7, 4]
truckSize2 = 6
print(getMaxUnits(boxes2, unitsPerBox2, truckSize2))

boxes2 = [3, 1, 1]
unitsPerBox2 = [2, 7, 4]
truckSize2 = 6
print(getMaxUnits(boxes2, unitsPerBox2, truckSize2))
