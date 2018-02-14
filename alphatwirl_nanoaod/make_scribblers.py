from scribblers.obj import Collection
from scribblers.nanoaod_dataset_info import DatasetInfo
from scribblers.in_certified_lumi_sections import in_certified_lumi_sections
from scribblers.nanoaodtools_module_wrapper import NanoaodtoolsModuleWrapper
from scribblers.cutflowId import cutflowId
from scribblers.MetNoX import MetNoX
from scribblers.OverlapRemoval import OverlapRemoval

from object_selection import ObjectSelection

import os

class Test(object):
    """
    Test class to print info on event loop"
    """
    def event(self, event):
        print event.Jet
        print event.JetSelection
        print event.JetVeto
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

    # Object vetoes
    jet_veto = dict(All = (
        'j: j.pt>40.',
        'j: abs(j.eta)<5.',
        'j: j.puId>=1', # loose
        'j: j.jetId>=1', # loose
    ))
    muon_veto = dict(All = (
        'u: u.pt>10.',
        'u: abs(u.eta)<2.4',
        'u: abs(u.dxy)<0.118',
        'u: abs(u.dz)<0.882',
    ))
    electron_veto = dict(All = (
        'e: e.pt>10.',
        'e: abs(e.eta)<2.1',
        'e: abs(e.dxy)<0.5',
        'e: abs(e.dz)<1.0',
        'e: e.miniPFRelIso_all<0.1',
        'e: e.lostHits<=1',
        'e: e.cutBased>=1', # Veto or higher
    ))
    photon_veto = dict(All = (
        'y: y.pt>25.',
        'y: abs(y.eta)<2.5',
        'y: y.cutBased>=1', # Loose of higher
    ))

    # Object selections
    jet_selection = dict(All = (
        'j: abs(j.eta)<2.4',
    ))
    muon_selection = dict(All = (
        'u: u.pt>30.',
        'u: abs(u.eta)<2.1',
        'u: u.tightId',
    ))
    electron_selection = dict(All = (
        'e: e.pt>30.',
        'e: abs(e.eta)<2.1',
        'e: e.cutBased>=4', # Tight or higher
    ))
    photon_selection = dict(All = (
        'y: y.pt>165.',
        'y: abs(y.eta)<1.45',
        'y: y.cutBased>=3', # Tight or higher
    ))

    obj_attrs = ['pt','eta','phi']


    return [
        Collection("Jet", attrs=obj_attrs+["puId","jetId"]),
        Collection("Muon", attrs=obj_attrs+["dxy","dz","miniPFRelIso_all","tightId","jetIdx"]),
        Collection("Electron", attrs=obj_attrs+["dxy","dz","miniPFRelIso_all","lostHits","cutBased","jetIdx"]),
        Collection("Photon", attrs=obj_attrs+["cutBased","jetIdx"]),
        Collection("Tau", attrs=obj_attrs),
        ObjectSelection(in_obj_name="Muon",
                        out_obj_name="MuonVeto",
                        path_cfg=muon_veto
        ),
        ObjectSelection(in_obj_name="MuonVeto",
                        out_obj_name="MuonSelection",
                        path_cfg=muon_selection
        ),
        ObjectSelection(in_obj_name="Electron",
                        out_obj_name="ElectronVeto",
                        path_cfg=electron_veto
        ),
        ObjectSelection(in_obj_name="ElectronVeto",
                        out_obj_name="ElectronSelection",
                        path_cfg=electron_selection
        ),
        ObjectSelection(in_obj_name="Photon",
                        out_obj_name="PhotonVeto",
                        path_cfg=photon_veto
        ),
        ObjectSelection(in_obj_name="PhotonVeto",
                        out_obj_name="PhotonSelection",
                        path_cfg=photon_selection
        ),
        ObjectSelection(in_obj_name="Jet",
                        out_obj_name="JetVeto",
                        path_cfg=jet_veto
        ),
        OverlapRemoval(collection_name="JetVeto",
                       ref_collection="MuonVeto",
        ),
        OverlapRemoval(collection_name="JetVeto",
                       ref_collection="ElectronVeto",
        ),
        OverlapRemoval(collection_name="JetVeto",
                       ref_collection="PhotonVeto",
        ),
        ObjectSelection(in_obj_name="JetVeto",
                        out_obj_name="JetSelection",
                        path_cfg=jet_selection
        ),
        DatasetInfo(),
        json_scribbler,
        cutflowId(),
        MetNoX(),
        #leptonsf_scribbler,
        #jecunc_scribbler,
        #btagsf_scribbler,
    ]
