list = [5,2,4,6,2,10]

def lowest_value(list):
    minValue = list[0]
    for i in range(len(list)):
        if list[i] < minValue:
            minValue = list[i]

    return minValue

print(lowest_value(list))