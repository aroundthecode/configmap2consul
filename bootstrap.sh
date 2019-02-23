#!/usr/bin/env bash
virtualenv -p python3 venv
source ./venv/bin/activate
pip install -e ".[test]"

echo source ./venv/bin/activate
