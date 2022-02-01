Why this project exists
=======================

This project and post, `like this previous post <http://hselab.org/pip_conda_local_dev.html>`_ was inspired by numerous frustrating
attempts to create a simply analytics related package with the following characteristics:

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


## A simple analytics project

Many of my analytics projects involve simulation or optimization models. Usually there
are YAML formatted config files that get read in and there are usually csv files
that get written as output. Almost always there is the notion of different scenarios
that one might analyze and each scenario usually gets its own YAML config file.

For this simple demonstration project, I'm creating an application that generates $n$
random variates from an Erlang distribution. Erlang distributions are commonly used in stochastic
modeling and are the sum of $k$ exponential distributions, each having mean $b$. Depending on the value of
$k$, the erlang distribution takes on unimodal shapes ranging from exponential ($k=1$) through
right skewed, symmetric and finally a spike ($k=\infinity$).

The user inputs are some sort of scenario identifier, $k$, $b$ and $n$. The outputs will include things like a csv file
of the $n$ random variates as well as a text file containing summary statistics along
with a graphics file containing a histogram and overlaid theoretical probability distribution function.

## Main module to be both runnable and importable

## Simple CLI based on ``argparse``
## Reading from input files and writing output files
## Inputs can be specified using a YAML config file
## External and internal imports
## Use ``src`` folder layout
## Use within a conda virtual environment
## Installing in "editable (development) mode" using ``pip``
## Uses ``pytest`` for basic unit tests as well as testing the CLI
## Install locally with ``pip`` into conda environment
## Deploy to GitHub

