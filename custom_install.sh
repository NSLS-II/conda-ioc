#!/bin/bash

if [ ! -d "pcaspy" ]; then
    git clone https://github.com/paulscherrerinstitute/pcaspy
fi

echo "* Ensuring pcaspy is installed"
conda install --yes swig
pushd pcaspy
python setup.py install
popd

if [ ! -d "pypvserver" ]; then
    git clone https://github.com/klauer/pypvserver
fi

echo "* Ensuring pypvserver is installed"
pushd pypvserver
python setup.py develop
popd
