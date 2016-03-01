#!/bin/bash

# source init.sh

source config

export CONDA_ENV
export CONDA_ROOT
export PACKAGES

export PATH="$CONDA_ROOT/bin:$PATH"

source activate $CONDA_ENV
python ioc_main.py || sleep 5.0
