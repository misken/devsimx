def erlangb(load, c):
    """
    Return the the probability of loss in M/G/c/c system using recursive approach.

    Much faster than direct computation via
    scipy.stats.poisson.pmf(c, load) / scipy.stats.poisson.cdf(c, load)

    Parameters
    ----------
    load : float
        average arrival rate * average service time (units are erlangs)
    c : int
        number of servers

    Returns
    -------
    float
        probability arrival finds system full

    """

    invb = 1.0
    for j in range(1, c + 1):
        invb = 1.0 + invb * j / load

    b = 1.0 / invb

    return b


def erlangc(load, c):
    """
    Return the the probability of delay in M/M/c/inf system using recursive Erlang B approach.


    Parameters
    ----------
    load : float
        average arrival rate * average service time (units are erlangs)
    c : int
        number of servers

    Returns
    -------
    float
        probability all servers busy

    """

    rho = load / float(c)
    if rho >= 1.0:
        raise ValueError("Traffic intensity >= 1.0")

    eb = erlangb(load, c)
    ec = 1.0 / (rho + (1 - rho) * (1.0 / eb))

    return ec