import numpy as np

m = np.array(range(2,27))
print(m)
print()

m = m.reshape(5,5)
print(m)
print()

m[1:4,1:4] = 0
print(m)
print()

m = m@m
print(m)
print()

x = np.sqrt(m[0]@m[0])
print(x)
print()