# alphatwirl-NanoAOD
Adaptors to interface to the nanoAODTools code to process nanoAOD files.

### Why isn't this in alphatwirl or alphatwirl-interface?
Because nanoAOD is CMS-specific (and developmental) and this projet includes the nanoAOD-tools as a submodule.
Alphatwirl aims to be experiment agnostic.
If ever there's an alphatwirl-CMS project then this should become part of that.

## Setup
Install alongside a version of AlphaTwirl and make sure to do:
```
source setup.sh
```
in each clean shell that wants to use this
