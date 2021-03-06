from alphatwirl.loop import NullCollector
from alphatwirl.configure import TableConfigCompleter, TableFileNameComposer
from alphatwirl_interface.completions import complete
from alphatwirl_interface.nanoaod.runners import  build_job_manager

from cut_flow import cut_flow
from make_scribblers import make_scribblers
from df_builder import prepare_dataframe_configs
from save_tree import SaveTree

import os
import pprint
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.getLogger("alphatwirl").setLevel(logging.INFO)

import pandas as pd

class WithInsertTableFileNameComposer():
    def __init__(self, composer, inserts):
        self.inserts = inserts
        self.composer = composer
        self.frame_idx = 0

    def __call__(self, columnNames, indices, **kwargs):
        this_insert = self.inserts[self.frame_idx]
        suffix = kwargs.get("suffix", self.composer.default_suffix)
        kwargs["suffix"] = "--{}.{}".format(this_insert, suffix)
        self.frame_idx += 1
        return self.composer(columnNames, **kwargs)


def main(out_dir, mode, components, xrd_redirector="root://xrootd-cms.infn.it//",
         events_per_dataset=-1, events_per_process=-1, n_files=1, ncores=4,
         quiet=False):

    # Prepare the run manager
    user_modules=["alphatwirl_nanoaod","postprocessing", "scribblers"]
    mgr = build_job_manager(out_dir, parallel_mode=mode, force=True,
                            user_modules=user_modules, quiet=quiet,
                            max_events_per_dataset=events_per_dataset,
                            max_events_per_process=events_per_process,
                            max_files_per_run=n_files,
                            n_processes=ncores)

    # Choose components
    if not os.path.exists(components):
        raise IOError("File {} does not exist".format(components))
    components_df = pd.read_table(components,sep='\s+',comment='#')
    components_df["files"] = components_df["files"].apply(lambda fs:
            [f if "/store/"!=f[:7] else xrd_redirector+f for f in eval(fs)]
            )

    # Setup scribblers
    scribblers = make_scribblers()

    # Prepare the event selection
    event_selection = cut_flow(out_dir)

    # Describe the output dataframe
    df_cfg = prepare_dataframe_configs()

    # Run alphatwirl to build the dataframe
    dataframes = summarize(out_dir, mgr, df_cfg, event_selection, scribblers, components_df)

    # Print everything out
    dataframes = filter(lambda x: x is not None, dataframes)
    print "Number of objects created:",len(dataframes)
    for df in dataframes:
        print type(df)
        #pprint.pprint(df)


def summarize(out_dir, mgr, df_cfg, event_selection, scribblers, components_df):
    '''
        Summarise the data in the tree into the data frames (DFs) given in
        df_cfg.

        :param mgr: NANOAOD job manager
        :param df_cfg(list): list of DF definitions
        :param event_selection: pairs of event selections and collectors
        :param scribblers: pairs of scribblers and empty collectors which
                           create new event content
        :param components_df: list of nanoaod component names to summarize
    '''

    reader_collector_pairs = [(s,NullCollector()) for s in scribblers] + event_selection

    reader_collector_pairs += [(SaveTree(out_dir),NullCollector())]

    name_composer = WithInsertTableFileNameComposer(TableFileNameComposer(),
                                                    df_cfg.keys())
    # setting up defaults to complete the provided DF configs
    tableConfigCompleter = TableConfigCompleter(
        # using a composer to create a predictable output file name
        # based on the names of the output columns
        createOutFileName=name_composer,
        defaultOutDir=out_dir
    )
    # combine configs and completers
    reader_collector_pairs += complete(df_cfg.values(), tableConfigCompleter)

    print "Components:"
    for d,e in zip(components_df["dataset"],components_df["era"]):
        print "\t{}_{}".format(d,e)
    print

    return mgr.run(reader_collector_pairs, components=components_df)
