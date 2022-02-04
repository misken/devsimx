import simpy
import yaml
from numpy.random import RandomState

"""
Simple patient flow model

Details:

- Generate arrivals via Poisson process
- Uses one Resource objects to model an observation unit,
- Arrival rate, mean lengths of stay, and capacity of the OBS unit are read from YAML config file

"""
# Arrival rate and length of stay inputs.
ARR_RATE = 0.4
MEAN_LOS_OBS = 3
CAPACITY_OBS = 2

RNG_SEED = 6353


def patient_generator(env, arr_rate, prng=RandomState(0)):
    """Generates patients according to a simple Poisson process

        Parameters
        ----------
        env : simpy.Environment
            the simulation environment
        arr_rate : float
            exponential arrival rate
        prng : RandomState object
            Seeded RandomState object for generating pseudo-random numbers.
            See https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.RandomState.html

    """

    patients_created = 0

    # Infinite loop for generatirng patients according to a poisson process.
    while True:

        # Generate next interarrival time
        iat = prng.exponential(1.0 / arr_rate)

        # Generate length of stay in each unit for this patient
        los_obs = prng.exponential(MEAN_LOS_OBS)

        # Update counter of patients
        patients_created += 1

        # Create a new patient flow process.
        obp = obpatient_flow(env, 'Patient{}'.format(patients_created),
                             los_obs=los_obs)

        # Register the process with the simulation environment
        env.process(obp)

        # This process will now yield to a 'timeout' event. This process will resume after iat time units.
        yield env.timeout(iat)


def obpatient_flow(env, name, los_obs):
    """Process function modeling how a patient flows through system.

        Parameters
        ----------
        env : simpy.Environment
            the simulation environment
        name : str
            process instance id
        los_obs : float
            length of stay in OBS unit
    """

    print("{} trying to get OBS at {}".format(name, env.now))

    # Timestamp when patient tried to get OBS bed
    bed_request_ts = env.now
    # Request an obs bed
    bed_request = obs_unit.request()
    # Yield this process until a bed is available
    yield bed_request

    # We got an OBS bed
    print("{} entering OBS at {}".format(name, env.now))
    # Let's see if we had to wait to get the bed.
    if env.now > bed_request_ts:
        print("{} waited {} time units for OBS bed".format(name, env.now - bed_request_ts))

    # Yield this process again. Now wait until our length of stay elapses.
    # This is the actual stay in the bed
    yield env.timeout(los_obs)

    # All done with OBS, release the bed. Note that we pass the bed_request object
    # to the release() function so that the correct unit of the resource is released.
    obs_unit.release(bed_request)
    print("{} leaving OBS at {}".format(name, env.now))

# Initialize a simulation environment
env = simpy.Environment()

# Initialize a random number generator.
# See https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.RandomState.html
prng = RandomState(RNG_SEED)

# Declare a Resource to model OBS unit. Default capacity is 1, we pass in desired capacity.
obs_unit = simpy.Resource(env, CAPACITY_OBS)

# Run the simulation for a while
runtime = 250
env.process(patient_generator(env, ARR_RATE, prng))
env.run(until=runtime)