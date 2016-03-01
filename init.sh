#!/bin/bash

source deactivate

source config

export CONDA_ENV
export CONDA_ROOT
export PACKAGES

export PATH="$CONDA_ROOT/bin:$PATH"

echo $HOME
echo "PATH is $PATH"

CONDA_INSTALLER=Anaconda3-2.5.0-Linux-x86_64.sh
CONDA_INSTALLER_URL=https://repo.continuum.io/archive/Anaconda3-2.5.0-Linux-x86_64.sh

if [ ! -f $CONDA_INSTALLER ]; then
    echo "* Downloading miniconda"
    wget $CONDA_INSTALLER_URL
fi

if [ ! -d "$CONDA_ROOT" ]; then
    echo "* Installing miniconda"
    chmod +x $CONDA_INSTALLER
    ./$CONDA_INSTALLER -b -f -p $CONDA_ROOT/
fi

echo "* condarc:"
cat $HOME/.condarc

echo "* binstar config:"
cat $HOME/.config/binstar/config.yaml

echo "* Checking anaconda-client installation (required for nsls-ii packages)"
conda install anaconda-client --yes

echo "* Creating the conda environment, if necessary"
conda create -n $CONDA_ENV python=3.5 $PACKAGES -c $CONDA_CHANNEL --yes

echo "* Activating the '$CONDA_ENV' environment"
source activate $CONDA_ENV

echo "* This python executable will be used:"
which python

echo "* Installing any custom libraries, if necessary:"
source custom_install.sh

echo "* Python setup complete"
