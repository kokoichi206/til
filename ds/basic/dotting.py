import time
import numpy as np
import random


def dotting(a, b):
    return a.dot(b)

def looping(a, b):
    D = len(a)
    result = 0
    for i in range(D):
        result += a[i]*b[i]
    return result

if __name__ == '__main__':
    dim = 100_000_000

    a = [random.random() for _ in range(dim)]
    b = [random.random() for _ in range(dim)]
    start_time = time.time()
    looping(a, b)
    print("looping takes: " + str(time.time()-start_time))
    
    a = np.array(a)
    b = np.array(b)
    start_time = time.time()
    dotting(a, b)
    print("dotting takes: " + str(time.time()-start_time))
