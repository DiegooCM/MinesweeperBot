import numpy as np

a = np.array([[True, True, False], [True, True, True], [False, True, True]])
b = np.array([[1], [1], [1]])

#x = np.dot(np.linalg.inv(a), b)
x = np.linalg.solve(a,b)

print(f'x is {x[0]}, y-is {x[1]} and z-is {x[2]}')

