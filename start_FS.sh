#!/bin/bash
source /cvmfs/ship.cern.ch/SHiP-2023/May/setUp.sh
cd /afs/cern.ch/user/e/edursov/private/SIMULATIONS/my_FairShip/
source start_ali.sh
Condor_folder=/afs/cern.ch/user/e/edursov/private/SIMULATIONS/my_FairShip/muon/run_processing/
cd "$Condor_folder"
set -ux
echo "Starting script."
DIR=$1
SUB=$6
ProcId=$2
LSB_JOBINDEX=$((ProcId+1))
MUONS=$4
NTOTAL=$5
NJOBS=$3
TANK=6
ISHIP=3
MUSHIELD=8
N=$(( NTOTAL/NJOBS + ( LSB_JOBINDEX == NJOBS ? NTOTAL % NJOBS : 0 ) ))
FIRST=$(((NTOTAL/NJOBS)*(LSB_JOBINDEX-1)))
if eos stat "$EOS_DATA"/"$DIR"/"$LSB_JOBINDEX"/ship.conical.MuonBack-TGeant4.root; then
        echo "Target exists, nothing to do."
        exit 0
else

        python "$FAIRSHIP"/macro/run_simScript.py --muShieldDesign $MUSHIELD --MuonBack --nEvents $N --firstEvent $FIRST -f $MUONS --FastMuon -g scaled.root --stepMuonShield --output "$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/
        if [ "$LSB_JOBINDEX" -eq 1 ]; then
                xrdcp geofile_full.conical.MuonBack-TGeant4.root\
        root://eospublic.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/geofile_full.conical.MuonBack-TGeant4.root
        fi
fi
