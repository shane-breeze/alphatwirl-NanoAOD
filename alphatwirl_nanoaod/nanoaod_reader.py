

class FakeOutputTree(object):
    pass

class FakeInputTree(object):
    pass

class NanoAodReader(object):
    """
    """
    def __init__(self, module):
        # Not sure where we can call this, so put it here for now...
        # Might need to edit the AlphaTwirl loop to accommodate this
        self._module = module
        self._module.beginJob()

    def begin(self, events):
        return self._module.beginFile(inputFile, outputFile, inputTree, wrappedOutputTree)

    def event(self, event):
        return self._module.analyze(event)

    def end(self):
        return self._module.endFile(inputFile, outputFile, inputTree, wrappedOutputTree)

# Need to call this somewhere, although currently no module actually uses it
#    def endJob(self):                                                              
