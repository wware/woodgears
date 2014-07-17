#!/bin/sh

if [ ! -d venv ]
then
    virtualenv venv || exit 1
fi

source venv/bin/activate
pip install -r requirements.txt
