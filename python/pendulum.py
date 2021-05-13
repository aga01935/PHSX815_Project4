import sys
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

if __name__ == "__main__":

    Nexp = 1000
    # Input constants
    m = 1 # mass (kg)
    L = 1 # length (m)
    b = 0 # damping value (kg/m^2-s)
    g = 9.81 # gravity (m/s^2)
    delta_t = 0.02 # time step size (seconds)
    t_max = 20 # max sim time (seconds)
    theta1_0 = np.pi/2 # initial angle (radians)
    theta2_0 = 0.2 # initial angular velocity (rad/s)
    theta_init = (theta1_0, theta2_0)


    print (sys.argv[0])
    if '-Nexp' in sys.argv:
        p = sys.argv.index('-Nexp')
        Ne = int(sys.argv[p+1])
        if Ne > 0:
            Nexp = Ne
    if '-Tmax' in sys.argv:
        p = sys.argv.index('-Tmax')
        Ne = int(sys.argv[p+1])
        if Ne > 0:
            t_max = Ne

    if '-fname' in sys.argv:
        p = sys.argv.index('-fname')
        Ne = sys.argv[p+1]
        filename = Ne


    # Get timesteps
    t = np.linspace(0, t_max, int(t_max/delta_t))
    #print (t)

    # differential equation for the theta
    def int_pendulum_sim(theta_init, t, L=1, m=1, b=0.2, g=9.81):
        theta_dot_1 = theta_init[1]
        theta_dot_2 = -b/m*theta_init[1] - g/L*np.sin(theta_init[0])
        return theta_dot_1, theta_dot_2

    def g_calculator(time_period = 0, length = 1):
        return (length * (2*np.pi/time_period)**2)

    #solving the differntial equation
    meas_g = []
    OutputFileName = "result.txt"
    outfile = open(OutputFileName, 'w')

    for iter in range(0,Nexp):
        #integrating the equation to calcualte the value of theta and theta dot
        theta_vals_int = integrate.odeint(int_pendulum_sim, theta_init, t)
        #unfolding the value of theta and thetadot from the 2d list
        thetalist =[]
        thetadotlist =[]
        for item in theta_vals_int:
            thetalist.append(item[0])
            thetadotlist.append(item[1])
        #finding the peak or point of equilibrium
        peaks, _ = find_peaks(thetalist)
        #checking the time period of the oscillation
        #peakpoint =[]
        #peaktime =[]
        tperiod =[]
        # checking if the peak is identified properly
        for i in range(0,len(peaks)):
            #peakpoint.append(thetalist[peaks[i]])
            #peaktime.append(t[peaks[i]])
            if i <len(peaks)-1:
                #calculating the mean of the time period
                tp = t[peaks[i+1]]-t[peaks[i]]
                #randomly selecting the time period from gaussian distribution
                tmeas = np.random.normal(tp,0.2)
                tperiod.append(tmeas)
        #calculating the average of time period as we do it on normal experiments
        avgt = sum(tperiod)/float(len(tperiod))
        outfile.write(str(avgt)+" ")
    outfile.close()
        
