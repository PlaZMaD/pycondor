#!/bin/bash
cd $1
source /afs/cern.ch/work/e/ekurbato/public/fs_setups/master/setUp.sh
eval $(alienv -a slc9_x86-64 load FairShip/latest-master-release --no-refresh)
cd -
set -ux
echo "Starting script."
# temp=`echo $5 | tr -d '\''`
mkdir -p $out_dir
python $FAIRSHIP/macro/run_simScript.py $5 --nEvents $4 --firstEvent $3 -f $2 --output $out_dir
