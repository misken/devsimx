A Python analytics sample development project
=============================================

**tldr** - Sample Python project and cookiecutter for the kinds of analytics projects I do

* `Sample analytics project repo on GitHub <>`_
* `Associated cookiecutter repo on GitHub <>`_

Why I'm writing this blog post
------------------------------
Every time I create a new Python analytics related project, I feel like I need to
relearn/re-remember how to do some of the same things, using the same Google searches
and hodge podge of notes. This includes (but is not limited to):

* How do I setup my project to make testing and packaging easy?
* How do I make sure my project is both runnable and importable, and, structures the ``if __name__ == '__main__'`` code bits properly?
* How do I do setup logging for a project with multiple modules?
* How do I use ``argparse`` correctly within my project to create a flexible and testable CLI?
* How do I use YAML config files to specify user inputs and coordinate this with the CLI?
* How do I make sure both external and internal imports work correctly?
* What, if anything, should be in ``__init__.py``?
* What are all the "gotchas" involved in pip installing my project into a conda virtual env?
* What are all the "gotchas" involved in using ``pytest`` and ``python`` executables within a conda virtual env?

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

I figured I should just create a sample project (and associated cookiecutter) that included these characteristics
along with documentation on the hows and whys of the code and project structure. This blog post is part of this
sample project documentation. Hopefully this will make it easier to quickly jumpstart new Python analytics projects
and allow me to spend less time revisiting the same (very helpful) StackOverflow posts again and again.

**DISCLAIMER** Clearly, I'm not a professional Python software developer. I'm an academic who does
teaching, applied research and open source software development in the realm of analytics
and `open educational resources <http://www.sba.oakland.edu/faculty/isken/teaching.html>`_.

Overview of the demo project
----------------------------

Many of my analytics projects involve simulation, optimization or statistical/ML models and
some sort of custom function library.
Usually there are YAML formatted config files that get read in and there are usually csv/json/pkl files
that get written as output. Almost always there is the notion of different scenarios
that one might analyze and each scenario usually gets its own YAML config file.

For this simple demonstration project, I'm creating an application that has a few
different pieces to represent my typical project types:

Generate random variates from an Erlang distribution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Erlang distributions are commonly used in stochastic
modeling and are the sum of $k$ exponential distributions, each having mean $b$. Depending on the value of
$k$, the erlang distribution takes on unimodal shapes ranging from exponential ($k=1$) through
right skewed, symmetric and finally a spike ($k=\infinity$).

The user inputs are some sort of scenario identifier, $k$, $b$ and $n$. The outputs will include things like a csv file
of the $n$ random variates as well as a text file containing summary statistics along
with a graphics file containing a histogram and overlaid theoretical probability distribution function.

Simple patient flow simulation model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I do a lot of discrete event simulation work and use the `SimPy <>`_ module. I'll use a
very simple SimPy model of a patient flowing through a single hospital unit. I want to
be able to specify all necessary input parameters via YAML config files, do logging, and
write out detailed csv data files and plots. BTW, erlang distributions are often used to model
length of stay in such simulation models. The model should have a CLI and it should be
easy to do experiments in which I run many different scenarios.

Analytical function library
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Often I'll need to write some custom analytical function and use it within my application. In
this demo project I'm going to include queueing related functions for computing the probability
of being delayed in what is known as an $M/M/c$ queueing system. It's a basic multiserver queue (think
call center with multiple agents) with exponentially distributed interarrival (the first $M$)
and service times (the second $$M$. The $M$'s stand for *Markovian*.
See `M/M/c Queue <https://en.wikipedia.org/wiki/M/M/c_queue>` for more details.

There's actually two different common use cases.

**Case 1: The functions are part of this project**

In this case, the functions will live in a separate module within this project. I just
need to make sure they can be imported and used.

**Case 2: The functions are part of some other analytical library I have created**

Obviously, I need to make sure that this other library (that I wrote) is importable
within the conda virtual environment used for the current project. The tricky thing is
doing the ``pip`` install into the conda virtual env. This was the topic of my
`previous post mentioned above <http://hselab.org/pip_conda_local_dev.html>`_.

The high level plan
-------------------

The plan is to create a sample Python analytics project that hits the points mentioned above. The sample project
will live on GitHub in a public repo. In addition, I'll create a `cookiecutter <>`_ based on this same
sample project to make it easy for me to quickly get a new analytics Python project up and running.

In addition, this blog post, and other documentation files will remain as part of the project and the cookiecutter to
serve as a set of reminder notes and reference material. Also, I'm sure I'm not doing everything correctly
or in the best way, and the notes can evolve and be improved over time.

The technical details
----------------------

Use ``src`` folder layout
^^^^^^^^^^^^^^^^^^^^^^^^^^

Using a ``src`` folder seems to have gained momentum as the recommended way to lay out a Python project.

* Used in the official `sample Python project <https://github.com/pypa/sampleproject>`_ of PyPA
* This `2014 blog post <https://blog.ionelmc.ro/2014/05/25/python-packaging/>`_ still widely referenced

The open source book, `Python Packages <https://py-pkgs.org/04-package-structure>`_ has a ton of well-written,
detailed information and advice on packaging Python projects.

Here's what the sample project directory tree looks like: (TODO: Update this with final dir structure)

.. code::
    .
    ├── devsimx.yml
    ├── docs
    │    ├── conf.py
    │    ├── dev-notes.rst
    │    ├── getting-started.rst
    │    ├── index.rst
    │    ├── installation.rst
    │    ├── make.bat
    │    ├── Makefile
    │    ├── min_versions.rst
    │    ├── python-sample-dev-project.rst
    │    ├── release-history.rst
    │    └── usage.rst
    ├── LICENSE
    ├── notebooks
    │    ├── input
    │    └── output
    ├── README.md
    ├── requirements.txt
    ├── setup.py
    ├── src
    │    └── devsimx
    │        ├── __init__.py
    │        ├── input
    │        │    └── scenario_1.yaml
    │        ├── output
    │        │    └── test.csv
    │        ├── sim_erlang .py
    │        └── simio.py
    └── tox.ini

Main module to be both runnable and importable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I have included the standard check for ``__main__`` and moved all main logic (including CLI argument parsing)
to a ``main()`` procedure.

Wrapping the call to ``main()`` with ``sys.exit`` is
done `per the docs <https://docs.python.org/3/library/__main__.html#packaging-considerations>`_.

    By proactively following this convention ourselves, our module will have the
    same behavior when run directly (i.e. python3 echo.py) as it will have if we later
    package it as a console script entry-point in a pip-installable package.

Here's what the code looks like in ``sim_erlang.py`` at the module level.

.. code::
    if __name__ == '__main__':
        sys.exit(main())

The details of ``main()`` are discussed below when we talk about CLI argument parsing and the overall logic
flow of the application.

Simple CLI based on ``argparse``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All of the
arguments are optional keyword arguments with sensible default values. There is a ``--config`` argument that
takes a configuration filename in which all of the other input arguments can be set. Any input values set
via the config file will override any set via the command line. This makes it easy to
run multiple scenarios of this simulation by creating scenario specific configuration files. They are
YAML formatted files and the details are discussed below.

Currently there is no parameter input validation other than through specifying a ``type=`` attribute in
the ``add_argument`` method call.

.. code::
    parser.add_argument(
        '-n', type=int, default=1,
        help="Number of random variates to generate (default is 1)"
    )

The parser logic is in ``sim_erlang.process_command_line()`` which is called from ``main()``.  The call looks like this:

.. code::

    def main(argv=None):
        """
        Main program logic

        Parameters
        ----------
        argv : list of command line arguments (Default is None)

        Returns
        -------
        0 if no errors

        """

        # Get input arguments
        args = process_command_line(argv)

    # More code ....

and ``sim_erlang.process_command_line()`` looks like this:

.. code::
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
        parser = argparse.ArgumentParser(prog='sim_erlang    ',
                                         description='Generate erlang random variates')

        # Add arguments
        parser.add_argument(
            '-k', type=int, default=1,
            help="Number of stages in erlang distribution (default is 1)"
        )

        ... more add argument code

        args = parser.parse_args(argv)
        return args


If ``argv == None``, then ``parse_args`` will use ``sys.argv[1:]``.
By including ``argv=None`` as input to ``main``, our program can be
imported and ``main`` called with arguments. This will be useful for
testing via pytest.

More resources
~~~~~~~~~~~~~~~

* https://docs.python.org/3/howto/argparse.html
* https://realpython.com/command-line-interfaces-python-argparse/

Conda virtual environments: Setup and use
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PyCharm setup
^^^^^^^^^^^^^^

In **Settings | Tools | Python Integrated Tools**, set

* default testing to pytest
* default docstring format to NumPy




Conda virtual environments: External and internal imports
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Development dependencies vs install dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

requirements.txt vs setup.py

https://stackoverflow.com/questions/43658870/requirements-txt-vs-setup-py

https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/

    ``install_requires`` is a setuptools ``setup.py`` keyword that should be used to specify what a
    project minimally needs to run correctly. When the project is installed by pip, this is the
    specification that is used to install its dependencies.

https://dev.to/bowmanjd/python-dev-environment-part-3-dependencies-with-installrequires-and-requirements-txt-kk3

* Put dependencies needed for installation of the project by others in setup.py in install_requires parameter.

* Put dev dependencies needed by the developer in requirements.txt
    - Put -e . at top of requirements.txt
    - Put external dependencies next and include things like pytest and Sphinx if needed by dev
