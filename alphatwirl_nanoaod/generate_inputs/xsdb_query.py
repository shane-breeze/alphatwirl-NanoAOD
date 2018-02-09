import os
import sys
import numpy as np
import pandas as pd
import shlex
from subprocess import Popen, PIPE

def xsdb_query(df, out_file=None, attrs=["shower","mtrx_gen","cross_section","accuracy"], verbose=True):
    """
    Query XSDB webpage for dataset infos. Currently requires kerberos
    authentication to work (i.e. only works on lxplus)
    """
    # Loop over dataset querying using the "process_name"
    data = []
    for process_name in df["dataset"]:
        query = {"process_name": process_name}

        # I would very much appreciate it if people would write their code so
        # that a result is returned from a function rather than printing the
        # result to stdout. Rant over
        command = "python -c \"from request_wrapper import RequestWrapper; RequestWrapper().simple_search({})\"".format(query)
        p = Popen(shlex.split(command), stdout=PIPE, stdin=PIPE)
        stdout, stderr = p.communicate()
        result = eval(stdout)

        # len(result)==0 if there is not xsdb entry. Need to use the genXS tool
        if len(result)==0:
            if verbose:
                print "WARNING: No entry found for {}. Try using the genXS tool".format(process_name)
            data.append({k: np.nan for k in attrs})        
        else:
            data.append({k: eval(stdout)[0][k] for k in attrs})
    df_xsdb = pd.DataFrame(data, columns=attrs)
    result = pd.concat([df, df_xsdb], axis=1)
    if not out_file is None:
        result.to_csv(out_file,sep='\t')
    return result
