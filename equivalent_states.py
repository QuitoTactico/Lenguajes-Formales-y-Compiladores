with open('input.txt', 'r') as file:
    inputs = [i.split() for i in file.readlines()]

index = 1
for _ in int(inputs[0]):
    actual_len = int(inputs[index]) + 2
    for j in range(index, actual_len):



    index += actual_len