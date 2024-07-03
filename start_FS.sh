#!/bin/bash
source $1
eval $(alienv -w $2/sw -a slc9_x86-64 load FairShip/latest-master-release --no-refresh)
set -ux
echo "Starting script."
mkdir -p $out_dir
python $FAIRSHIP/macro/run_simScript.py ${@:6} --nEvents $5 --firstEvent $4 -f $3
cp *.root $out_dir 
