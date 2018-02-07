# Tai Sakuma <tai.sakuma@cern.ch>
import json

##__________________________________________________________________||
class in_certified_lumi_sections(object):
    def __init__(self, json_path):
        self.certifiedLumiSections = [ ]
        j = json.load(open(json_path))
        for run in sorted(j.keys()):
            for lumi_range in j[run]:
                lumis = range(lumi_range[0], lumi_range[1] + 1)
                self.certifiedLumiSections.extend([(int(run), ls) for ls in lumis])
        # e.g., self.certifiedLumiSections = [(256941, 137), (256941, 138), (256941, 139)]
        self.certifiedLumiSections = set(self.certifiedLumiSections)

    def begin(self, event):
        self.vals = [ ]
        event.inCertifiedLumiSections = self.vals

    def event(self, event):
        event.inCertifiedLumiSections = self.vals
        self.vals[:] = [(event.run[0], event.luminosityBlock[0]) in self.certifiedLumiSections]

##__________________________________________________________________||
