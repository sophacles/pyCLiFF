Introduction
============

pyCLiFF is the Python Command Line Filter Framework. It is designed to allow
developers to quickly create command line filter utilities.  These filter
utilities take text input, perform some sort of transform on that text, and
output it again. Most of the time these utilities are quick one-offs,
considered (at least initially) to be throwaway code. Such programs are
frequently very simple, requiring code rewrites to use in a simialar context,
or full of boiler plate code to allow use in multiple contexts.  pyCLiFF
provides that boilerplate, allowing fr the very simple writing of reusable
filters.

Command Line Filters -- an in-depth look
-----------------------------------------

The command line filter concept has it's hitory in unix and unix shells.  The
philosphy of these systems is that many small programs chained together can
create powerful composites.  The output of one program becomes the input of
another program. For example::

   $cat syslog | grep ERROR |head -n10

The above script actually runs three programs, :program:`cat`, :program:`grep`,
and :program:`head`.  :program:`cat` simply outputs the file :file:`syslog`.
:program:`grep` searches for text, in this case the string *ERROR*.
:program:`head` simply displays a maximum of n lines of output. The | symbol
means **pipe**, which is the name of the mechanism the shell uses to connect
the output of one command to the input of another. These pipelines can get very
complex and powerful, for a more in-depth treatment, see the
_wikipedia entry:http://en.wikipedia.org/wiki/Pipeline_(Unix)

Further, \*nix  systems provide a very large number of programs taylored to
processing the text throught pipelines.  Many of these commands are very
powerful and constitute mini programming languages in themselves. This is
frequently where problems arrise. Sometimes it is difficult to coerce a program
to output text exactly as needed, other times it is impossible to find the
right command or remember its syntax.  If the user knows a programming
language, like python, it is simpler to just write the correct peice
for the pipeline by hand. In such ways are new filters born.

These filters all seem to follow the same basic pattern:

1. Setup/handle arguments
2. Mainloop:
  A. Read line from input file (stdin or file)
  B. Process that line in some way
  C. Output the result of processing.
3. Cleanup and exit.

Further, each filter program seems to have a pretty common set of options. Such
things as turning off stderr output, or redirecting to an output file instead
of the stdout.  Not every filter needs every option, sometimes because those
options don't make sanse in context of the program, but more frequently because
they are too much work to add a simple program.

In any case, a pattern (like shown above) combined with a common set of
operations (such as the command line arguments), frequently leads to lots of
boring boilerplate.

Enter pyCLiFF
-------------

This is where pyCLiFF comes into play. It is designed to take the tedium out of
simple command line scripts. Say for example you want to output line numbers
with the text of a pipeline, with pyCLiFF it is as simple as::

    from pyCLiFF import CLF

    linenumber = 0
    def process(line):
        global linenumber
        linenumber +=1
        return "%d: %s" % (linenumber, line)
    CLF(processdata=process).main()

Thats it. :program:`pyCLiFF` takes care of the rest. The main function opens
stdin and feeds it, line-by-line, into the process function.  It will then
display the return value on stdout.  Further, if the script (lets call it
:progname:`number.py`) is not in the middle (or end) of a pipeline, but is
instead first, we could pass it a positional argument like so::

    $number.py file

And :program:`pyCLiFF` will automatically know to look in file for its input instead of
stdin.

There is a bit more to :program:`pyCLiFF`, but not much, it is designed to be
simple and stay out of the way. Some other features include:

* Built in stderr messaging.
* Silence standard error with -q
* output and/or input from files instead of stdin/stdout
* add your own command line options


