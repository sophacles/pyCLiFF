#!/usr/bin/env python

import optparse, sys, os

'''
standard options:
 -o output filename
 -f config filename (defaults to CLF.configfile, then to ~/.progname)
 -q turn off error messages

arguments:
    first arg (args[0] after optparse) is the source file, if none use
    sys.stdin
'''
class CLF(object):
    configfile = ''
    output_mode = 'w' #could be a if we want i guess
    def __init__(self, **kw):
        self.__OP = optparse.OptionParser()

        # configfile stuff
        if 'configfile' in kw:
            self.configfile = kw[configfile]
        if not self.configfile:
            self.configfile = os.path.expanduser(\
                '~/.%s' % self.__OP.get_prog_name())

        # standard options
        self.add_arg('-f','--configfile', dest = 'configfile',\
            help= "Alternate configfile location instead of %s" %\
            self.configfile)
        self.add_arg('-o','--outfile', dest='outfile',
            help="Put the output in the file instead of stdout")
        self.add_arg('-q', '--quiet', action='store_true', default=False,
            help="Quiet mode, don't print messages to stderr")
        # options provided
        for opt in kw.get('options',[]):
            self.add_arg(*opt[0], **opt[1])

        # add the handling functions if they are not defined because
        # we are subclassing. This is a bit wierd, but neded because of
        # the multiple ways to use this.

        if not hasattr(self, 'handle_opts'):
            self.handle_opts = kw.get('handle_opts',(lambda *args: None))
        if not hasattr(self, 'handle_params'):
            self.handle_params = kw.get('handle_params',(lambda *args: None))
        if not hasattr(self, 'handle_config'):
            self.handle_config = kw.get('handle_config',(lambda *args: None))

        # so this is different than above, because under no circumstances does
        # it make sense to not have a processdata function
        if not hasattr(self, 'processdata'):
            try:
                self.processdata = kw['processdata']
            except KeyError:
                raise AttributeError("Must specify a way to handle the data")

        self.tagline = kw.get('tagline', '')
        self.issetup = False

    def add_arg(self, *args, **kw):
        self.__OP.add_option(*args, **kw)

    def config(self):
        if not self.confighandler: return
        fd = open(self.configfile, 'r')
        data = fd.read()
        fd.close()
        self.confighandler(data)

    def handle_cl(self):
        opts, params = self.__OP.parse_args()

        self.__outfile_name = opts.outfile
        if opts.configfile:
            self.configfile = opts.configfile

        if opts.quiet:
            sys.stderr.close()

        # user options handler
        self.handle_opts(opts)

        if params:
            self.__infile_name = params[0]
            # user parameters handler
            self.handle_params(params[1:])
        else:
            self.__infile_name = ''

    def setup(self):
        # different usage of this module could result in this being called
        # more than once...
        if self.issetup: return

        self.handle_cl()
        self.handle_config()

        # input setup
        if self.__infile_name:
            self.infile = open(self.__infile_name, 'r')
        else:
            self.infile = sys.stdin

        # output setup
        if self.__outfile_name:
            self.outfile = open(self.__outfile_name, self.output_mode)
        else:
            self.outfile = sys.stdout

        self.issetup = True

    def finish(self):
        self.infile.close()
        if self.tagline:
            self.outfile.write(self.tagline())
        self.outfile.close()

    def message(self, m):
        '''write a message to stderr, if it is open. This makes for easy
        parsing/handling of the -q option'''
        if not m.endswith('\n'):
            m = m + '\n'
        if not sys.stderr.closed: # why don't python file objects have a .opened?
            sys.stderr.write(m)


    def main(self):
        self.setup()
        while True:
            indata = self.infile.readline()
            if not indata: break
            try:
                outdata = self.processdata(indata)
            except StopIteration:
                break
            self.outfile.write(outdata)
            self.outfile.flush()
        self.finish()
