#!/bin/bash
#cd $2
source $1
eval $(alienv -a -w $2/sw slc9_x86-64 load FairShip/latest-master-release --no-refresh)
#cd -
set -ux
echo "Starting script."
# temp=`echo $5 | tr -d '\''`
mkdir -p $out_dir
python $FAIRSHIP/macro/run_simScript.py ${@:6} --nEvents $5 --firstEvent $4 -f $3
#--output $out_dir
cp *.root $out_dir 
