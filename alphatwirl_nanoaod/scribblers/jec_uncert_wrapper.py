from postprocessing.modules.jme.jecUncertainties import jecUncertProducer

##__________________________________________________________________||
class event_wrapper(object):
    def __init__(self, event):
        # can't assign it as an attribute because I'm reassigning the
        # __getattr__ member function -> self.event would give an infinite loop
        # there
        self.__dict__["event"] = event

    def __getattr__(self, attr):
        val = getattr(self.__dict__["event"], attr)
        if val.array.typecode in ("h", "H", "i", "I"):
            return val[0]
        return val

    def __setattr__(self, attr, val):
        setattr(self.__dict__["event"], attr, val)

##__________________________________________________________________||
class tree_wrapper(object):
    def set_event(self, event):
        self.event = event

    def branch(self, name, *args, **kwargs):
        setattr(self, name, [])
        setattr(self.event, name, getattr(self, name))

    def fillBranch(self, name, val):
        setattr(self.event, name, getattr(self, name))
        if type(val) == list:
            getattr(self, name)[:] = val
        else:
            getattr(self, name)[:] = [val]

##__________________________________________________________________||
class nanoaodtools_module_wrapper(object):
    def __init__(self, *args, **kwargs):
        self.nanoaod_tools_module = jecUncertProducer(*args, **kwargs)
        self.tree = tree_wrapper()

    def begin(self, event):
        self.tree.set_event(event)
        self.nanoaod_tools_module.beginFile(None, None, None, self.tree)
        self.nanoaod_tools_module.beginJob()
        self.wrapped_event = event_wrapper(event)

    def event(self, event):
        self.tree.set_event(event)
        self.nanoaod_tools_module.analyze(self.wrapped_event)

##__________________________________________________________________||
