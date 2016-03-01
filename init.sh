#!/bin/bash

source deactivate

source config

export CONDA_ENV
export CONDA_ROOT
export PACKAGES

export PATH="$CONDA_ROOT:$PATH"

if [ ! -f "Miniconda3-latest-Linux-x86_64.sh" ]; then
    echo "* Downloading miniconda"
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
fi

if [ ! -d "$CONDA_ROOT" ]; then
    echo "* Installing miniconda"
    chmod +x Miniconda3-latest-Linux-x86_64.sh
    ./Miniconda3-latest-Linux-x86_64.sh -b -f -p $CONDA_ROOT/
fi

echo "* Creating the conda environment, if necessary"
conda create -n $CONDA_ENV python=3.5 $PACKAGES --yes

echo "* Activating the '$CONDA_ENV' environment"
source activate $CONDA_ENV

echo "* This python executable will be used:"
which python

echo "* Installing any custom libraries, if necessary:"
source custom_install.sh

echo "* Python setup complete"
