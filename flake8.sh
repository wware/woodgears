#!/bin/sh

flake8 $(find . -name '*.py' | grep -v deprecated | grep -v venv)
