#/bin/bash

if [ ! -d .venv ] 
then
    echo "building venv ..."
    python3 -m venv .venv
fi

source .venv/bin/activate
echo "upgrading and install modules..."
python3 -m pip install --upgrade pip >> /dev/null
pip install jinja2 >> /dev/null
python3 build-plugin-dev-environment.py