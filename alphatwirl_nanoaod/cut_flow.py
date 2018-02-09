"""
Define the cut flow for the pseudo-RA1 analysis
"""

import os
from alphatwirl_interface.cut_flows import cut_flow_with_counter

baseline_selection = dict(Any = (
    dict(All = ('ev: ev.isdata[0]', 'ev: ev.inCertifiedLumiSections[0]')),
    dict(All = ('ev: not ev.isdata[0]',)),
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
