import random
import numpy as np

def decay_sim(thalf, N0=500, tgrid=None, nhalflives=4):
    """Simulate the radioactive decay of N0 nuclei.

    thalf is the half-life in some units of time.
    If tgrid is provided, it should be a sequence of evenly-spaced time points
    to run the simulation on.
    If tgrid is None, it is calculated from nhalflives, the number of
    half-lives to run the simulation for.

    """

    # Calculate the lifetime from the half-life.
    tau = thalf / np.log(2)

    if tgrid is None:
        # Create a grid of Nt time points up to tmax.
        Nt, tmax = 100, thalf * nhalflives
        tgrid, dt = np.linspace(0, tmax, Nt, retstep=True)
    else:
        # tgrid was provided: deduce Nt and the time step, dt.
        Nt = len(tgrid)
        dt = tgrid[1] - tgrid[0]

    N = np.empty(Nt, dtype=int)
    N[0] = N0
    # The probability that a given nucleus will decay in time dt.
    p = dt / tau
    for i in range(1, Nt):
        # At each time step, start with the undecayed nuclei from the previous.
        N[i] = N[i-1]
        # Consider each nucleus in turn and decide whether it decays or not.
        for j in range(N[i-1]):
            r = random.random()
            if r < p:
                # This nucleus decays.
                N[i] -= 1
    return tgrid, N


N0 = 500
# Half life of 14C in years.
thalf = 5730

# Use Nt time steps up to tmax years.
Nt, tmax = 100, 20000
tgrid = np.linspace(0, tmax, Nt)

# Repeat the simulation "experiment" nsims times.
nsims = 10
Nsim = np.empty((Nt, nsims))
for i in range(nsims):
    _, Nsim[:, i] = decay_sim(thalf, N0, tgrid)

# Save the time grid, followed by the simulations in columns. We save integer
# values for the data and create a comma-delimited file with a two-line header.
np.savetxt('14C-sim.csv', np.hstack((tgrid[:, None], Nsim)),
    fmt = '%d', delimiter=',',
    header=f'Simulations of the radioactive decay of {N0} 14C nuclei.\n'
           f'Columns are time in years followed by {nsims} decay simulations.'
          )
