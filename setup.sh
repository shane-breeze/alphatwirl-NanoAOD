# export PYTHONPATH=$PYTHONPATH:externals/alphatwirl:externals/alphatwirl-interface
# 
# # Set up the python path and source the nanoAOD stand-alone scripts
# export ALPHATWIRL_NANOAOD_ROOT="$(dirname $BASH_SOURCE)"
# if [[ "$ALPHATWIRL_NANOAOD_ROOT" == .* ]];then
#     ALPHATWIRL_NANOAOD_ROOT="$PWD${ALPHATWIRL_NANOAOD_ROOT/.}"
# fi
# 
# # Wrap all the nanoAOD output with a prefix
# ECHO="$(which echo)"
# function echo(){
#   $ECHO "NanoAOD-tools:" $@
# }
# if [ ! -d $ALPHATWIRL_NANOAOD_ROOT/externals/nanoAOD-tools/build ];then
#     (
#     source $ALPHATWIRL_NANOAOD_ROOT/externals/nanoAOD-tools/standalone/env_standalone.sh build
#     )
# fi
# source $ALPHATWIRL_NANOAOD_ROOT/externals/nanoAOD-tools/standalone/env_standalone.sh
# 
# unset echo
# unset ECHO
# export PYTHONPATH="${ALPHATWIRL_NANOAOD_ROOT}/alphatwirl_nanoaod/${PYTHONPATH:+:${PYTHONPATH}}"

Fast_cvmfs_PythonDir=/cvmfs/sft.cern.ch/lcg/releases/Python/2.7.13-597a5/x86_64-slc6-gcc62-opt/
Fast_cvmfs_PipDir=/cvmfs/sft.cern.ch/lcg/releases/pip/8.1.2-c9f5a/x86_64-slc6-gcc62-opt/
Fast_cvmfs_GCCSetup=/cvmfs/sft.cern.ch/lcg/contrib/gcc/6.2/x86_64-slc6/setup.sh
Fast_cvmfs_RootSetup=/cvmfs/sft.cern.ch/lcg/releases/LCG_88/ROOT/6.08.06/x86_64-slc6-gcc62-opt/bin/thisroot.sh

if [ -z "$(which root-config 2>/dev/null)" ] \
    || [[ "$(root-config --version)" != 6.* ]] ;then
    if [ -r "${Fast_cvmfs_RootSetup}" ] && [ -r "$Fast_cvmfs_GCCSetup" ]; then
      source "${Fast_cvmfs_GCCSetup}"
      source "${Fast_cvmfs_RootSetup}"
    else
      echo "Cannot setup ROOT 6 and it doesn't seem to be configured already, this might be an issue..."
    fi
fi

FAST_top_dir(){
  local Canonicalize="readlink -f"
  $Canonicalize asdf &> /dev/null || Canonicalize=realpath
  dirname "$($Canonicalize "${BASH_SOURCE[0]}")"
}

export FAST_RA1_ROOT="$(FAST_top_dir)"
export FAST_RA1_EXTERNALS_DIR="$(FAST_top_dir)/externals"

FAST_build_some_path(){
  local NewPath="$1" ;shift
  for dir in "$@";do
    if ! $( echo "$NewPath" | grep -q '\(.*:\|^\)'"$dir"'\(:.*\|$\)' ); then
      NewPath="${dir}${NewPath:+:${NewPath}}"
    fi
  done
  echo "$NewPath"
}

FAST_build_path(){
  local Dirs=( "${FAST_RA1_ROOT}"/bin "${FAST_RA1_EXTERNALS_DIR}"/pip/bin )
  Dirs+=( {"$Fast_cvmfs_PythonDir","$Fast_cvmfs_PipDir"}/bin)
  FAST_build_some_path "$PATH" "${Dirs[@]}"
}

FAST_build_python_path(){
  local Dirs=( "${FAST_RA1_ROOT}" "${FAST_RA1_EXTERNALS_DIR}"/{alphatwirl,alphatwirl-interface,aggregate,pip/lib/python2.7/site-packages} )
  Dirs+=( {"$Fast_cvmfs_PythonDir","$Fast_cvmfs_PipDir"}/lib/python2.7/site-packages/)

  FAST_build_some_path "$PYTHONPATH" "${Dirs[@]}"
}

export PYTHONPATH="$(FAST_build_python_path)"
export PATH="$(FAST_build_path)"

# Special treatment needed for setuptools
python -m pip install --prefix "${FAST_RA1_EXTERNALS_DIR}"/pip -U setuptools
python -m pip install --prefix "${FAST_RA1_EXTERNALS_DIR}"/pip -r requirements.txt

PS1_PREFIX=alphatwirl-nanoaod

unset FAST_build_some_path
unset FAST_build_path
unset FAST_build_python_path
unset Fast_cvmfs_PythonDir
unset Fast_cvmfs_PipDir
unset Fast_cvmfs_GCCSetup
unset Fast_cvmfs_RootSetup

