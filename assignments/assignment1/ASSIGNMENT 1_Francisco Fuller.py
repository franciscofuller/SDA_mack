
#======================================================================================
# SCIENTIFIC DATA ANALYSIS
#
# FRANCISCO A G FULLER
# 722.5599-4

# ASSIGNMENT 1
# 
# a) Write a Python function that returns a function f(x) that is a Gaussian 
#    function, given as input an array of x and the function parameters p as a list. 
# 
# b) Write a Python script to that uses the previous function to make a plot,
#    given the input parameters, x and p. Find the Gaussian parameters
#    to best fit the function to the following data set:
# 
# x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# y = [-2.72621128e-02,  1.81646869e-04, -4.08932157e-04,  1.17070532e-01, 
#      5.81937187e-01,  5.92375028e-01,  1.19868306e-01, -1.27347601e-02, 
#      9.49023422e-03, -1.13061490e-02]
# 
# c) Show the results in a plot with the dataset and your best-fit function
# 
# Upload you Python notebook .ipynb ou script .py to Moodle by 6th Sept. 2023, 18:30.
#
#======================================================================================

# THE CODE:

import numpy as np
import math
import matplotlib.pyplot as plt




def Function_Gauss(X,a):
    
# X = serie of data
# a = amplitude (Y)
    
    mean = sum(X) / len(X)
    variance = sum((i - mean) ** 2 for i in X) / len(X)
    std_dev = math.sqrt(variance)

    Gauss = np.arange(0.0000, len(X))
    for i in range(0, len(X)):
        Gauss[i] = (  1/(std_dev * np.sqrt(2 * np.pi))  ) * np.exp(-(1/2)*((X[i]-mean)/std_dev)**2)
    Gauss_Ampl = np.arange(0.0000, len(X))
    for i in range(0, len(X)):
        Gauss_Ampl[i] = (  a[i]  ) * np.exp(-(1/2)*((X[i]-mean)/std_dev)**2)
    
    return Gauss, Gauss_Ampl


def Plot_Gauss(X, a):


    Gauss, Gauss_Ampl = Function_Gauss(X,a)
    
    plt.plot(X,Gauss,alpha=1,color='orange', label = 'Data X')
    plt.plot(X,Gauss,'.',color='chocolate')
        
    plt.plot(X,Gauss_Ampl,alpha=1,color='blue', label = 'Data Y and X')
    plt.plot(X,Gauss_Ampl,'.',color='c')
        
    plt.grid()
    plt.legend()
    plt.xlabel('X axis')
    plt.ylabel('g(x)')
    plt.title('Gaussian function');
    plt.show()

    return X, Gauss, Gauss_Ampl


# THE DATA


X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

y = [-2.72621128e-02, 1.81646869e-04, -4.08932157e-04, 1.17070532e-01,

     5.81937187e-01, 5.92375028e-01, 1.19868306e-01, -1.27347601e-02,

     9.49023422e-03, -1.13061490e-02]

# THE EXECUTION

X, Gauss, Gauss_Ampl = Plot_Gauss(X, y)


