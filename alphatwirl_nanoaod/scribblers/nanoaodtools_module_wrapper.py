import sys
import os
import importlib

##__________________________________________________________________||
class EventWrapper(object):
    def __init__(self, event):
        self.__dict__["event"] = event

    def __getattr__(self, attr):
        if attr.startswith("__"):
            raise AttributeError(attr)
        val = getattr(self.__dict__["event"], attr)
        if val.array.typecode in ("h", "H", "i", "I"):
            return val[0]
        return val

    def __setattr__(self, attr, val):
        setattr(self.__dict__["event"], attr, val)

##__________________________________________________________________||
class TreeWrapper(object):
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
class NanoaodtoolsModuleWrapper(object):
    def __init__(self, module_path, module_name, *args, **kwargs):
        nanoaodtools_module = importlib.import_module(module_path)
        self.nanoaodtools_module = getattr(nanoaodtools_module, module_name)(*args, **kwargs)
        self.tree = TreeWrapper()

    def begin(self, event):
        self.tree.set_event(event)
        self.nanoaodtools_module.beginFile(None, None, None, self.tree)
        self.nanoaodtools_module.beginJob()
        self.wrapped_event = EventWrapper(event)

    def event(self, event):
        self.tree.set_event(event)
        self.nanoaodtools_module.analyze(self.wrapped_event)

##__________________________________________________________________||
