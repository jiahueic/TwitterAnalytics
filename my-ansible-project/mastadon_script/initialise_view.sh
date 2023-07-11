#!/bin/bash
. ./venv/bin/activate
python3 mastadon_id.py --ip $1 --db $2
