# alphatwirl-NanoAOD
Adaptors to interface to the nanoAODTools code to process nanoAOD files.

### Why isn't this in alphatwirl or alphatwirl-interface?
Because nanoAOD is CMS-specific (and developmental) and this projet includes the nanoAOD-tools as a submodule.
Alphatwirl aims to be experiment agnostic.
If ever there's an alphatwirl-CMS project then this should become part of that.

## Setup
To get nanoAODTools' modules to work you need CMSSW. I suggest you follow the
setup of nanoAOD (<https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD#Recipe_for_CMSSW_9_4_X_and_the_c>)
and the do `cmsenv` before sourcing the setup script for the repository.

Install alongside a version of AlphaTwirl and make sure to do:
```
source setup.sh
```
in each clean shell that wants to use this

## How to run

### Generate input dataframe
The input dataframes has a dataset per row which tell AlphaTwirl all the
required information for each dataset. Also get MC info such as XS from xsdb
(only works at lxplus so far).

To generate the dataframe run:
```
python bin/dataset_query -o data/components.csv "/*/*/NANOAODSIM"
```
where `-o` specifies the output and the positional argument is the DAS dataset
query (`-i` specifies the instance to send to `dasgoclient`)

You can open the dataframe in the file and comment lines out as you want using
'#'

### Run AlphaTwirl over nanoAOD
To run AlphaTwirl over nanoAOD run the following command:
```
python bin/trees2dataframes --components data/components.csv --n-files 1
```
Use the help to see the full set of options. I have had issues when using
`--n-files` greater than 1 (memory issues), so keep it at 1 for now.

## TODO
* Create a weight for MC to scale the genWeight up to the XS and desired
  luminosity, dealing with multiple extensions
* Create scribblers for standard variables: MHT, alphaT, bdphi, ... (might
  already exist in some repo somewhere)
* Create a scribbler to use the delR matched index in nanoAOD objects to remove
  objects from a collection (i.e. remove muons matched to jets)
* Update the event selection. Requires the baseline selection, cutflow
  selections and data/mc specific selections.
* Create tbls for the pu reweighting, btag SF, JECs, ... (other corrections) to
  allow for the plotting of some distributions before and after applying the
  correction
