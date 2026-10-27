import numpy as np

def func(pi1, pi, q):
    return np.cross(pi1-pi,q-pi)
q = np.array([17,16,0])
p1 = np.array([14,20,0])
p2 = np.array([15,11,0])
p3 = np.array([20,13,0])
p4 = np.array([18,23,0])
print(func(p2,p1,q))
print(func(p3,p2,q))
print(func(p4,p3,q))
print(func(p1,p4,q))