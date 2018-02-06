from subprocess import Popen, PIPE
import shlex
import pandas as pd

def run_command(command, dry_run=False):
    p = Popen(shlex.split(command), stdout=PIPE, stderr=PIPE)
    return p.communicate()

def query_dataset(dataset):
    summary_command = 'dasgoclient --query "summary dataset={}" --limit 0'.format(dataset)
    out, err = run_command(summary_command)
    summary = eval(out)[0]

    files_command = 'dasgoclient --query "file dataset={}" --limit 0'.format(dataset)
    out, err = run_command(files_command)
    files = out.split()

    return summary, files

def main(dataset_query):
    dataset_command = 'dasgoclient --query "dataset={}" --limit 0'.format(dataset_query)
    out, err = run_command(dataset_command)
    datasets = out.split()

    data = []
    for dataset in datasets:
        dataset_name, era, tier = dataset.split("/")[1:]
        event_type = "MC" if "SIM" in tier else "Data"
        summary, files = query_dataset(dataset)

        if "NANOAOD" not in tier:
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
    print df
    return df

if __name__ == "__main__":
    df = main("/SingleMuon/*/NANOAOD")
