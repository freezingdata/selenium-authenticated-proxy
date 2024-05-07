#!/bin/bash
set -e

for py_version in 3.10 3.11 3.12
do
    echo "Creating python=$py_version environment for test..."
    ~/miniconda3/bin/conda create -n test_env python=$py_version -y > /dev/null
    ~/miniconda3/bin/conda run -n test_env pip install -r requirements.txt > /dev/null
    ~/miniconda3/bin/conda run -n test_env pytest test --cache-clear
    ~/miniconda3/bin/conda env remove --name test_env -y > /dev/null
    find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
    rm -rf selenium_authenticated_proxy/tmp
    rm -rf test/__pycache__
    rm -rf .pytest_cache
done
