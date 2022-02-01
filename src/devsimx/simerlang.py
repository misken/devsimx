import sys
from datetime import datetime

import logging
from pathlib import Path
import argparse

import numpy as np
from numpy.random import default_rng

import yaml


"""
Generate random samples from an erlang-k distribution

Background
==========

This project is meant to be a template for analytics software development projects
that I do. See 

Details
=======

* main module to be both runnable and importable,
* has a simple CLI based on ``argparse``,
* involves reading from YAML input config files and writing csv output files,
* input arguments passed on command line override values set by config file (if exists),
* imports from various common libraries such as ``numpy`` but also imports from modules in this package,
* uses ``src`` folder layout,
* usable within a conda virtual environment,
* uses ``pytest`` for basic unit tests as well as testing the CLI,
* intended to be locally ``pip`` installed,
* during development, works correctly when installed in "editable mode"
* deploy to GitHub (not worrying about publishing to PyPI or Conda Forge for now)

Planned enhancements from obflow_5:

Goal is to be able to run new scenarios for the obsim experiments. Model
needs to match Simio model functionality.

- LOS distributions that match the obsim experiments
- LOS adjustment in LDR based on wait time in OBS
- logging
- read key scenario inputs from a file

Key Lessons Learned:

- Any function that is a generator and might potentially yield for an event
  must get registered as a process.

"""


def process_command_line(argv=None):
    """
    Parse command line arguments

    Parameters
    ----------
    argv : list of arguments, or `None` for ``sys.argv[1:]``.

    Returns
    ----------
    Namespace representing the argument list.
    """

    # Create the parser
    parser = argparse.ArgumentParser(prog='simerlang',
                                     description='Generate erlang random variates')

    # Add arguments
    parser.add_argument(
        '-k', type=int, default=1,
        help="Number of stages in erlang distribution (default is 1)"
    )

    parser.add_argument(
        '-b', type=float, default=1.0,
        help="Overall mean of erlang distribution (i.e., each stage has mean b/k). (default is 1.0)"
    )

    parser.add_argument(
        '-n', type=int, default=1,
        help="Number of random variates to generate (default is 1)"
    )

    parser.add_argument(
        '--scenario', type=str, default=f'scen{datetime.now():%Y%m%d%H%M}',
        help="String used in output filenames"
    )

    parser.add_argument(
        '-o', '--output', type=str, default=sys.stdout,
        help="Path to directory in which to output files"
    )

    parser.add_argument(
        '-s', type=int, default=None,
        help="Random number generator seed (default is None)"
    )

    parser.add_argument(
        '--config', type=str, default=None,
        help="Configuration file containing input parameter arguments and values"
    )

    parser.add_argument("--loglevel", default='WARNING',
                        help="Use valid values for logging package (default is 'WARNING")

    # Do the parsing and return the populated namespace with the input arg values
    # If argv == None, then ``parse_args`` will use ``sys.argv[1:]``.
    # By including ``argv=None`` as input to ``main``, our program can be
    # imported and ``main`` called with arguments. This will be useful for
    # testing via pytest.
    args = parser.parse_args(argv)
    return args


def generate_rvs(k=1, b=1, n=1, seed=None):
    """

    Parameters
    ----------
    k : int, number of stages (default is 1)
    b : float, overall mean of erlang distribution (default is 1)
    n : int, number of erlang variates to generate (default is 1)
    seed : int, seed for random number generator (default is None)

    Returns
    -------
    samples : ndarray

    """
    if seed is None:
        logging.warning("No random number generator seed specified.")

    rng = default_rng(seed)
    logging.info(f'k={k}, b={b}, n={n}')
    rvs = rng.gamma(shape=k, scale=b / k, size=n)

    return rvs


def rvs_tocsv(rvs, args):
    """
    Export random variates to csv

    This would often be a pandas dataframe. Simple 1d array, for now, is written.

    Parameters
    ----------
    rvs : ndarray
    args : namespace

    Returns
    -------
    No return value, the ``rvs`` data written to ``args.output``.

    """
    np.savetxt(args.output, rvs, delimiter=',')
    logging.info(f'random variates written to {args.output}')


def update_args(args, config):
    """
    Update args namespace values from config dictionary

    Parameters
    ----------
    args : namespace
    config : dict

    Returns
    -------
    Updated args namespace
    """

    # Convert args namespace to a dict
    args_dict = vars(args)
    logging.info(f'args passed = {args_dict}')

    # Update args dict from config dict
    for key in config.keys():
        args_dict[key] = config[key]

    logging.info(f'args post config = {args_dict}')
    # Convert dict to updated namespace
    args = argparse.Namespace(**args_dict)
    return args


def main(argv=None):
    """

    :param argv:
    :return:
    """
    # Get input arguments
    args = process_command_line(argv)

    # Setup logging
    loglevel = args.loglevel
    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    # Update input args if config file passed
    if args.config is not None:
        # Read inputs from config file
        with open(args.config, 'rt') as yaml_file:
            yaml_config = yaml.safe_load(yaml_file)
            args = update_args(args, yaml_config)

    logging.info(args)

    # Generate erlang random variates
    erlang_variates = generate_rvs(k=args.k, b=args.b, n=args.n, seed=args.s)

    # Handle output
    if args.output is not None:
        rvs_tocsv(erlang_variates, args)
        print(erlang_variates)
    else:
        print(erlang_variates)

    return 0


if __name__ == '__main__':
    sys.exit(main())
