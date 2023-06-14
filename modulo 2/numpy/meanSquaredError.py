import numpy as np


def MSE(a,b):
    mse = np.mean((a-b)**2)
    return mse

def MAE(a, b):
    mae = np.mean(np.abs(a - b))
    return mae

a = np.array([0,1,2,6,8])
b = np.array([3,1,6,2,1])

print("MSE = ", MSE(a,b))
print("MAE = ", MAE(a,b))