from alphatwirl.loop import NullCollector
from alphatwirl.configure import TableConfigCompleter, TableFileNameComposer
from alphatwirl_interface.completions import complete
from alphatwirl_interface.nanoaod.runners import  build_job_manager

from scribblers.in_certified_lumi_sections import in_certified_lumi_sections
from scribblers.jec_uncert_wrapper import nanoaodtools_module_wrapper

from cut_flow import cut_flow
from df_builder import prepare_dataframe_configs

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
    user_modules=["alphatwirl_nanoaod"]
    mgr = build_job_manager(out_dir, parallel_mode=mode, force=True,
                            user_modules=user_modules, quiet=quiet,
                            max_events_per_dataset=events_per_dataset,
                            max_events_per_process=events_per_process,
                            max_files_per_run=n_files,
                            n_processes=ncores)

    # Choose components
    components_df = pd.read_table("data/components2016.csv",sep='\t',index_col=0,comment='#')
    components_df["files"] = components_df["files"].apply(
            lambda fs: [f if "/store/"!=f[:7] else xrd_redirector+f for f in eval(fs)]
            )

    # Setup scribblers
    json_path = os.path.join(os.getcwd(), "data/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt")
    scribblers = [
            in_certified_lumi_sections(json_path),
            nanoaodtools_module_wrapper("Summer16_23Sep2016V4_MC"),
            ]

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
        pprint.pprint(df)


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

    return mgr.run(reader_collector_pairs, components=components_df)
