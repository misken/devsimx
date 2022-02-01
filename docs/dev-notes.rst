Development notes
==================

## Use ``src`` folder layout

Here's what the project directory tree looks like:



## Main module to be both runnable and importable

Included the standard check for ``__main__`` and moved all main logic (including argument parsing)
to a ``main()`` procedure.

.. code::
    if __name__ == '__main__':
        sys.exit(main())

## Simple CLI based on ``argparse``

The parser logic is in ``process_command_line`` which is called from ``main(argv=None)``.

If argv == None, then ``parse_args`` will use ``sys.argv[1:]``.
By including ``argv=None`` as input to ``main``, our program can be
imported and ``main`` called with arguments. This will be useful for
testing via pytest.

## Reading from input files and writing output files
## Inputs can be specified using a YAML config file

If a config file path is passed as one of the input arguments, any argument values
specified in the config file will update current input argumement values set via
command line flags or default values. I added an ``update_args`` function that
gets called after command line is parsed and ``config`` is not equal to ``None``.

## External and internal imports
## Basic logging that works with internal imports

## Use within a conda virtual environment
## Installing in "editable (development) mode" using ``pip`` into a conda environment
## Uses ``pytest`` for basic unit tests as well as testing the CLI
## Deploy to GitHub


