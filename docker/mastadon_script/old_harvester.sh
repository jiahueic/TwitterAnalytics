#!/bin/bash
. ./venv/bin/activate
python old_harvester.py --tag $1 --ip $2
