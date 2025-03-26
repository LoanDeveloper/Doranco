arr = [2,3,0,2,3,2]

def counting_sort(array):
    countArray = [0] * (max(array) + 1)
    arraySort = []
    for i in array:
        countArray[i] += 1
    print(countArray)
    for i in range(len(countArray)):
        #print(countArray[i])
        for j in range(countArray[i]):
            print("j : " + str(j) + " countArray : " + str(countArray[i]))
            #print("i : " + str(i))
            arraySort.append(i)
    return arraySort

print(counting_sort(arr))