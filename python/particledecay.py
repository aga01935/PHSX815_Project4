#referenced this from
##https://scipython.com/book2/chapter-6-numpy/examples/simulating-radioactive-decay/
import random
import numpy as np

def particle_decay_simulator(halflife, N0=500, Granularity=None, nhalflives=4):


    # Calculate the lifetime from the half-life.
    Tau = halflife / np.log(2)

    if Granularity is None:
        # Create a grid of Nt time points up to tmax.
        Nt, tmax = 100, halflife * nhalflives
        Granularity, dt = np.linspace(0, tmax, Nt, retstep=True)
    else:
        # Granularity was provided: deduce Nt and the time step, dt.
        Nt = len(Granularity)
        dt = Granularity[1] - Granularity[0]

    N = np.empty(Nt, dtype=int)
    N[0] = N0
    # The probability that a given nucleus will decay in time dt.
    p = dt / Tau
    for i in range(1, Nt):
        # At each time step, start with the undecayed nuclei from the previous.
        N[i] = N[i-1]
        # Consider each nucleus in turn and decide whether it decays or not.
        for j in range(N[i-1]):
            r = random.random()
            if r < p:
                # This nucleus decays.
                N[i] -= 1
    return Granularity, N


N0 = 500
# Half life of 14C in years.
halflife = 5730

# Use Nt time steps up to tmax years.
Nt, tmax = 100, 20000
Granularity = np.linspace(0, tmax, Nt)

# Repeat the simulation "experiment" nsims times.
nsims = 10
Nsim = np.empty((Nt, nsims))
for i in range(nsims):
    _, Nsim[:, i] = particle_decay_simulator(halflife, N0, Granularity)

# Save the time grid, followed by the simulations in columns. We save integer
# values for the data and create a comma-delimited file with a two-line header.
np.savetxt('14C-sim.csv', np.hstack((Granularity[:, None], Nsim)),
    fmt = '%d', delimiter=',',
    header=f'Simulations of the radioactive decay of {N0} 14C nuclei.\n'
           f'Columns are time in years followed by {nsims} decay simulations.'
          )
