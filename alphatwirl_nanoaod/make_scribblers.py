from alphatwirl.selection.modules.LambdaStr import LambdaStr

from scribblers.obj import Collection
from scribblers.selection import ObjectSelection
from scribblers.nanoaod_dataset_info import DatasetInfo
from scribblers.in_certified_lumi_sections import in_certified_lumi_sections
from scribblers.nanoaodtools_module_wrapper import NanoaodtoolsModuleWrapper

import os

class test(object):
    def __init__(self, string):
        self.string = string

    def begin(self, event):
        self.Jet = event.Jet

    def event(self, event):
        print self.string, self.Jet
        for j in event.Jet:
            print self.string, j.pt
            print self.string, j.eta
        print

def make_scribblers():
    # JSON scribbler. Produces:
    # - inCertifiedLumiSections [bool]
    json_path = os.path.join(os.getcwd(), "data/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt")
    json_scribbler = in_certified_lumi_sections(json_path)

    # PUWeight. Produces:
    # - puWeight [float]
    puweight_scribbler = NanoaodtoolsModuleWrapper(
        "postprocessing.modules.common.puWeightProducer",
        "puWeight",
        mc_only=True,
    )

    # lepton SF. Produces:
    # - Muon_effSF
    # - Electron_effSF
    leptonsf_scribbler = NanoaodtoolsModuleWrapper(
        "postprocessing.modules.common.lepSFProducer",
        "lepSF",
        mc_only=True,
    )

    # JEC Uncs. Produces:
    # - Jet_jecUncert*
    jecunc_scribbler = NanoaodtoolsModuleWrapper(
        "postprocessing.modules.jme.jecUncertainties",
        "jecUncert",
        mc_only=True,
    )

    # JetMET Uncs. Produces:
    # - Jet_pt_smeared
    # - MET_{pt,phi}_smeared
    # - Jet_pt_{jer,jes*,unclustEn}{Up,Down}
    # - MET_{pt,phi}_{jer,jes*,unclustEn}{Up,Down}
    jetmetunc_scribbler = NanoaodtoolsModuleWrapper(
        "postprocessing.modules.jme.jetmetUncertainties",
        "jetmetUncertainties",
        mc_only=True,
    )

    # BTagSF. Produces:
    # - Jet_btagSF
    # - Jet_btagSF_{up,down}
    btagsf_scribbler = NanoaodtoolsModuleWrapper(
        "postprocessing.modules.btv.btagSFProducer",
        "btagSF",
        mc_only=True,
    )

    # Object selections
    jet_selection = LambdaStr("j: j.pt>40. and abs(j.eta)<2.4")
    muon_selection = LambdaStr("u: u.pt>30. and abs(u.eta)<2.1")
    electron_selection = LambdaStr("e: e.pt>30. and abs(e.eta)<2.1")
    photon_selection = LambdaStr("y: y.pt>30. and abs(y.eta)<2.1")

    # Object vetoes
    jet_veto = LambdaStr("j: j.pt>40. and abs(j.eta)>2.4")
    muon_veto = LambdaStr("u: u.pt>30. and abs(u.eta)<2.1")
    electron_veto = LambdaStr("e: e.pt>30. and abs(e.eta)<2.1")
    photon_veto = LambdaStr("y: y.pt>30. and abs(y.eta)<2.1")

    obj_attrs = ["pt","eta","phi"]

    return [
        Collection("Jet", attrs=obj_attrs),
        Collection("Muon", attrs=obj_attrs),
        Collection("Electron", attrs=obj_attrs),
        Collection("Photon", attrs=obj_attrs),
        Collection("Tau", attrs=obj_attrs),
        ObjectSelection("Jet", "VetoJet", jet_veto),
        ObjectSelection("Jet", "Jet", jet_selection),
        ObjectSelection("Muon", "VetoMuon", muon_veto),
        ObjectSelection("Muon", "Muon", muon_selection),
        ObjectSelection("Electron", "VetoElectron", electron_veto),
        ObjectSelection("Electron", "Electron", electron_selection),
        ObjectSelection("Photon", "VetoPhoton", photon_veto),
        ObjectSelection("Photon", "Photon", photon_selection),
        DatasetInfo(),
        json_scribbler,
        #leptonsf_scribbler,
        #jecunc_scribbler,
        #btagsf_scribbler,
    ]
