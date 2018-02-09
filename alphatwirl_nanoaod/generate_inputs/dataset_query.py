from subprocess import Popen, PIPE
import shlex
import os
import pandas as pd

pd.set_option('display.max_colwidth', -1)

DASGOCLIENT_TEMPALTE = 'dasgoclient --query "{command} dataset={dataset} instance={instance}" --limit 0'

def run_command(command, dry_run=False):
    p = Popen(shlex.split(command), stdout=PIPE, stderr=PIPE)
    return p.communicate()

def query_dataset(dataset, instance):
    summary_command = DASGOCLIENT_TEMPALTE.format(
            command="summary",
            dataset=dataset,
            instance=instance,
            )
    out, err = run_command(summary_command)
    summary = eval(out)[0]

    files_command = DASGOCLIENT_TEMPALTE.format(
            command="file",
            dataset=dataset,
            instance=instance,
            )
    out, err = run_command(files_command)
    files = out.split()

    return summary, files

def main(dataset_query, out_file=None, instance="prod/global"):
    dataset_command = DASGOCLIENT_TEMPALTE.format(
            command="dataset",
            dataset=dataset_query,
            instance=instance,
            )
    out, err = run_command(dataset_command)
    datasets = out.split()

    data = []
    for dataset in datasets:
        dataset_name, era, tier = dataset.split("/")[1:]
        event_type = "MC" if "SIM" in tier else "Data"
        summary, files = query_dataset(dataset, instance)

        if instance=="prod/global" and "NANOAOD" not in tier:
            raise ValueError("This only supports NANOAOD")

        data.append({
            "eventtype": event_type,
            "dataset": dataset_name,
            "era": era,
            "nevents": summary["nevents"],
            "nfiles": summary["nfiles"],
            "files": files,
            })

    df = pd.DataFrame(data, columns=["eventtype", "dataset", "era", "nevents", "nfiles", "files"])

    if out_file is not None:
        if os.path.exists(out_file):
            df_existing = pd.read_csv(out_file,sep='\t',index_col=0,comment='#')
            df_existing["files"] = df_existing["files"].apply(eval)
            df = pd.concat([df_existing, df]).reset_index(drop=True)
        df.to_csv(out_file,sep='\t')
    return df

if __name__ == "__main__":
    df = main("/SingleMuon/*/NANOAOD")