#this is to analyze the pendulum experiment

import matplotlib.pyplot as plt
import numpy as np

L =1
g = 9.8
InputFile = "result.txt"

def g_calculator(time_period = 0, length = 1):
    return (length * (2*np.pi/time_period)**2)

meas_g = []
with open(InputFile) as ifile:

    for line in ifile:
        lineVals = line.split()
        for t in lineVals:
            g_temp = g_calculator(float(t), L)
            meas_g.append(g_temp)




plt.figure()
plt.hist(meas_g,bins =30,density = 0)
plt.axvline(g,color ="r",label = "True_value of g = 9.8 m/" +r"$s^2$")
plt.xlabel("g calculated ")
plt.ylabel("Probability")
plt.legend()
plt.show()
