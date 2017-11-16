# Set up the python path and source the nanoAOD stand-alone scripts
export ALPHATWIRL_NANOAOD_ROOT="$(dirname $BASH_SOURCE)"
if [[ "$ALPHATWIRL_NANOAOD_ROOT" == .* ]];then
    ALPHATWIRL_NANOAOD_ROOT="$PWD${ALPHATWIRL_NANOAOD_ROOT/.}"
fi

# Wrap all the nanoAOD output with a prefix
(
if [ ! -d $ALPHATWIRL_NANOAOD_ROOT/externals/nanoAOD-tools/build ];then
    bash $ALPHATWIRL_NANOAOD_ROOT/externals/nanoAOD-tools/standalone/env_standalone.sh build
fi
source $ALPHATWIRL_NANOAOD_ROOT/externals/nanoAOD-tools/standalone/env_standalone.sh
) 2>&1 |while read line; do
    echo NanoAOD-tools: $line
done

export PYTHONPATH="${ALPHATWIRL_NANOAOD_ROOT}/alphatwirl_nanoaod/${PYTHONPATH:+:${PYTHONPATH}}"
