Using the pyCLiFF Library
=========================

The pyCLiFF library is designed around the user supplied function:
**processdata**. This function is the main filter, and takes line of text, and
returns a line of text. This function is the only required part of a filter
built using pyCLiFF.  It can be thought of as a callback, which is triggered
every time the :program:`pyCLiFF` main loop encounters a line of text. Other
callbacks exist, and will be handled below.

To run a :program:`pyCLiFF` simply instantiate a CLF object and run its
mainloop.  The CLF class is created with options and callbacks specified in
it's contstuctor, as well as the processdata function::

    CLF(optins=[(('-n','--numlins'),{'default':10, "type":int"}),
                (('-L','--line-numbers'),
                 {'action':'store_true','default':False})],
         processdata = datafunc,
         handle_opts = optfunc)

It has one method for public calling: *main* () which is called to enter the
:program:`pyCLiFF` mainloop. This method will return after there is no more
data to process from the file or stdin.

Extra Options and Arguments
---------------------------

Options
^^^^^^^

:program:`pyCLiFF` takes advantage of python's optparse module. This module
allows for the trivial building of complex command line argument systems.  See
the relevent documentation in the python standard library for more information
on its use.  To create arguments for a filter program, simply pass a list to
the CLF object at instatiation. This list should consist of tuples. Each tuple
will be passed to th optparse.OptionParser.add_option() method. These tuples
should be composed such that the first element is a tuple for \*args and the
second a dict for \*\*kwargs.

There are also built in options which are used for extra functionality. These
are:

-q, --quiet
  Turn off stderr to reduce output.

-o, --outfile
  A file to write output, replaces stdout.

-f, --configfile
  A file to load configuration from.

Options are to be handled by the filter via the callback handle_opts.

Arguments
^^^^^^^^^

Postional arguments are also allowed by :program:`pyCLiFF`. The first
positional argument is always interpreted as the input filename.  Additional
arguments may be handled by the program, and will be passed via the
handle_params callback.

Callbacks
----------

Callbacks are defined by the CLF class, and used to pass control back to the
filter for user defined functionality.  Each of these callbacks will be called
once, during setup. They are functions passed to the CLF.__init__ method, as a
keyword argument. (See example above).

handle_opts(values)
  This callback is passed an optparse.OptionValues object, and is called in the
  setup phase of CLF.main, before the other callbacks, but after builtin option
  handling.

handle_params(params)
  This callback is passed a list of all positional parameters except the first,
  which is used internally to the CLF object. This will be called immediately
  after hanlde_opts is called, but will only be called if there are positional
  parameters to pass.

handle_config(data)
  This callback will be called if the command is called with the -f option. It
  will be passed data consisting of the contents of the file specified by -f.

In all cases for callbacks, if one is not specified a null operation will be
called instead, no callbacks are mandatory even if extra command line options
are specified.

Subclassing CLF
---------------

If the user chooses to subclass CLF instead of instantiating a CLF instance, it
is ok. This is expected behavior.  There are a few gotchas to watch out for
however:

1. Any callback which is implemented in the subclass and also passed as an
argument in __init__ will always ignore the argument in favour of the subclass
implementation.

2. If the subclass overrides main() it should call CLF.setup to handle command
line arguments and callbacks.

3. There is no 3.


