import re
import numpy as np
from datetime import *
import threading


# this func get input a list of shape (n,1) and check if it is a valid column or row or square
def listValidation(l):
    for x in l:
        # print(x)
        if int(x) < 1 or int(x) > 9:
            return False
    if list(dict.fromkeys(l)).__len__() < 9:
        return False
    return True


# this func calculate the index of members of a square and finally return a proper list for func listValidation
# the inputs are the matrix and number of square (start with 0 to 8)
def chooseSquare(lis, k):
    divide_3 = k // 3
    left_over_3 = k % 3

    l = [(x, y) for x in range(divide_3 * 3, divide_3 * 3 + 3) for y in range(3 * left_over_3, 3 * left_over_3 + 3)]
    # print(l)
    l = [lis[x][y] for x, y in l]
    # print(l)
    return l


# this func check what check to be done!? in other words it determine according to ch (number of square
# or 'c' for column or 'r' for row what list(or lists) be checked for validation
def sudokuValidation(li, ch):
    global return_value
    if 'r' == ch:
        for x in li:
            return_value = return_value and listValidation(x)
        # global return_value
        return_value = return_value and True
    elif 'c' == ch:
        for x in list(map(list, zip(*li))):
            # global return_value
            return_value = return_value and listValidation(x)
            # global return_value
        return_value = return_value and True
    else:
        # global return_value
        return_value = return_value and listValidation(chooseSquare(li, int(ch)))


# this func check calculate the execution time for every thread
def executeThreadWithTimePeriod(thread, j):
    timePass = datetime.now()
    thread.start()
    # print(thread.join())
    timePass = datetime.now() - timePass
    # print(time[i])
    # current_time = time[i].strftime("%H:%M:%S")
    print("thread #" + str(j) + " executes in " + str(timePass))


n = 9  # size of matrix n*n
input_file_path = "sudoku.txt"
file = open(input_file_path)
string = file.read()
# print(string)
inputs = re.split('\s', string)
# print(inputs)
# inputs.remove(inputs[inputs.__len__() - 1])  # delete last element
inputs = list(np.array(inputs).reshape(n, n))  # change the 1D-list with shape=(81,1) to 2D-list with shape=(9,9)
# print(inputs[1])
threads = []

# return_value is the final result the determines that the sudoku was valid or no
return_value = True
for i in range(0, n):
    threads.append(threading.Thread(target=sudokuValidation, args=(inputs, str(i))))

threads.append(threading.Thread(target=sudokuValidation, args=(inputs, 'c')))
threads.append(threading.Thread(target=sudokuValidation, args=(inputs, 'r')))

# print(threads.__len__())
for i in range(0, threads.__len__()):
    # sudokuValidation(inputs,i)
    executeThreadWithTimePeriod(threads[i], i)
# sudokuValidation(inputs,1)
print("result: " + ("valid" if return_value else "non valid" )+ " solution")
