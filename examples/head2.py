from pyCLiFF import CLF

class head(object):
    def __init__(self, **kw):
        self.lineno = 0
        self.maxline = kw.get('max', 10)
        self.fmt = kw.get('fmt', "%(line)s")
        self.myfilter = CLF(options= [(('-n',),{'type':'int', 'default':10}),
                                (('-L', '--number-lines'), {'dest':'num', 'action':'store_true'})],
                    handle_opts = self.handle_opts, processdata=self.datahandler)


    def handle_opts(self, opts):
        self.maxline = opts.n
        if opts.num:
            self.fmt = "%(lineno)s: %(line)s"

    def datahandler(self, line):
        if self.lineno >= self.maxline:
            raise StopIteration

        self.lineno += 1
        vals = self.__dict__.copy()
        vals.update(locals())
        return self.fmt % vals

    def run(self):
        self.myfilter.main()


if __name__ == '__main__':
    x = head()
    x.run()
