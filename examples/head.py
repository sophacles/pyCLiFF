'''Globals are bad evil and wrong, but its a down and dirty cl filter
so who actually cares? Are you gonna blog about me promoting bad one-off
practice?'''

from pyCLiFF import CLF

n = 0
clmax = 0
fmt = "%(line)s"

def handle_opts(opts):
    global clmax, fmt
    clmax = opts.n
    if opts.num:
        fmt = "%(n)s: %(line)s"

def datahandler(line):
    global n
    if n >= clmax:
        raise StopIteration

    n += 1
    vals = locals().copy()
    vals.update(globals())
    return fmt % vals


myfilter = CLF(options= [(('-n',),{'type':'int', 'default':10}),
                         (('-L', '--number-lines'), {'dest':'num', 'action':'store_true'})],
               handle_opts = handle_opts, processdata=datahandler)

myfilter.main()
