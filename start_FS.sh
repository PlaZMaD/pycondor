#!/bin/bash
cd $1
source /afs/cern.ch/work/e/ekurbato/public/fs_setups/master/setUp.sh
eval $(alienv load FairShip/latest-master-release --no-refresh)
# source start_ali.sh
cd -
set -ux
echo "Starting script."


echo "python \"$FAIRSHIP\"/macro/run_simScript.py $5 --nEvents $4 --firstEvent $3 -f $2 --output $out_dir"
# xrdcp geofile_full.conical.MuonBack-TGeant4.root root://eospublic.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/geofile_full.conical.MuonBack-TGeant4.root
#         fi