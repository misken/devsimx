Development notes
==================

## Use ``src`` folder layout

Packaging a Python library blog post - https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
https://py-pkgs.org/04-package-structure

https://github.com/pypa/sampleproject

Here's what the project directory tree looks like:



## Main module to be both runnable and importable

Included the standard check for ``__main__`` and moved all main logic (including argument parsing)
to a ``main()`` procedure.

Wrapping the call to ``main()`` with ``sys.exit`` is
done `per the docs <https://docs.python.org/3/library/__main__.html#packaging-considerations>`_.

    By proactively following this convention ourselves, our module will have the
    same behavior when run directly (i.e. python3 echo.py) as it will have if we later
    package it as a console script entry-point in a pip-installable package.



.. code::
    if __name__ == '__main__':
        sys.exit(main())

## Simple CLI based on ``argparse``

The parser logic is in ``process_command_line`` which is called from ``main(argv=None)``.

If argv == None, then ``parse_args`` will use ``sys.argv[1:]``.
By including ``argv=None`` as input to ``main``, our program can be
imported and ``main`` called with arguments. This will be useful for
testing via pytest.

* https://docs.python.org/3/library/argparse.html#argumentparser-objects

## Reading from input files and writing output files
## Inputs can be specified using a YAML config file

If a config file path is passed as one of the input arguments, any argument values
specified in the config file will update current input argumement values set via
command line flags or default values. I added an ``update_args`` function that
gets called after command line is parsed and ``config`` is not equal to ``None``.

## External and internal imports

## Basic logging that works with internal imports

https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial

## Use within a conda virtual environment
## Installing in "editable (development) mode" using ``pip`` into a conda environment

## Uses ``pytest`` for basic unit tests as well as testing the CLI

Python CLI tested with argparse - https://www.youtube.com/watch?v=sv46294LoP8&t=464s

https://docs.pytest.org/en/6.2.x/

## Deploy to GitHub


