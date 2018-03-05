"""
Define the cut flow for the pseudo-RA1 analysis
"""

import os
from alphatwirl_interface.cut_flows import cut_flow_with_counter

mc_selection = dict(All = (
    'ev: not ev.isdata[0]',
))

met_trigger = dict(Any = (
    'ev: ev.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight[0]',
    'ev: ev.HLT_PFMETNoMu100_PFMHTNoMu100_IDTight[0]',
    'ev: ev.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight[0]',
    'ev: ev.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight[0]',
))
muon_trigger = dict(Any = (
    'ev: ev.HLT_IsoMu24[0]',
    'ev: ev.HLT_IsoTkMu24[0]',
))
electron_trigger = dict(Any = (
    'ev: ev.HLT_Ele27_eta2p1_WPLoose_Gsf[0]',
))
trigger_selection = dict(Any = (
    dict(All = ("ev: 'MET' in ev.comp_name", met_trigger)),
    dict(All = ("ev: 'SingleMuon' in ev.comp_name", muon_trigger)),
    dict(All = ("ev: 'SingleElectron' in ev.comp_name", electron_trigger)),
))

data_selection = dict(All = (
    'ev: ev.isdata[0]',
    'ev: ev.inCertifiedLumiSections[0]',
    trigger_selection,
))

baseline_selection = dict(All = (
    'ev: ev.cutflowId[0] >= 0', # Mu, Ele, Pho selection
    'ev: len(ev.JetSelection) > 0', # Require at least 1 selected jet
    'ev: len(ev.JetVeto) == len(ev.JetSelection)', # Veto fwd jets
    'ev: ev.JetSelection[0].pt > 100.', # Lead jet pT > 100
    'ev: ev.METNoX_pt[0] > 200.', # MET no X cut
    dict(Any = (
        mc_selection,
        data_selection,
    )),
))

def cut_flow(output_directory=None, cut_flow_filename="cut_flow_table.txt"):
    '''
        Defines all cuts that will be applied to input data

        TODO: Read this directly from a yaml file, allow the file to define cut aliases
        TODO: Have a way to inspect what variables this cut flow needs...
    '''
    # dictionary of selection criteria
    # the 'All' key denotes that an event has to pass all the listed cuts
    # other options are Any (or) and Not (inverse)
    # event (`ev`) refers to a single entry in the input tree
    # names and indices after that are the branch names
    event_selection = dict(All = (
        baseline_selection,
    ))

    # create a reader + collector pair for the cutflow
    # the collector will reject events and store the cut flow into a text file
    if output_directory:
        cut_flow_filename = os.path.join(output_directory, cut_flow_filename)
    return cut_flow_with_counter(event_selection, cut_flow_filename)
