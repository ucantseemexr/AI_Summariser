def getMaxProfit(pnl, k):
    maximum = 0
    for i in range(1, k + 1):
        for j in range(len(pnl) - i + 1):
            total = sum(pnl[j:j + i])
            if total >= maximum:
                maximum = total
                
    return maximum

myArr1 =  [4, 3, -2, 9, -4, 2, 7]
k1 = 6
print(getMaxProfit(myArr1, k1))
myArr2 =  [2, 5, -7, 8, -6, 4, 1, -9]
k2 = 5
print(getMaxProfit(myArr2, k2))
myArr3 =  [-3, 4, 3, -2, 2, 5]
k3 = 4
print(getMaxProfit(myArr3, k3))

myArr4 =  [0, 1, 0, 0]
k4 = 1
print(getMaxProfit(myArr4, k4))