import htcondor
import classad
import pandas as pd
import os
import glob
import numpy as np

run_tag = "first_run"
debug = True
extra_fs_args = r'\" --fastMuon --MuonBack\"'
path_to_fs = "/afs/cern.ch/work/e/ekurbato/public/fs_setups/master"

events_per_job = 250000



output_dir = '/eos/experiment/ship/user/ekurbato/condor_output/'
log_dir = "/afs/cern.ch/work/e/ekurbato/public/condor_logs/"

output_dir = os.path.join(output_dir, run_tag)
input_files_db = pd.read_csv('input_for_muon_prod.txt', header=None)
input_files_db.columns=['path', 'nEvents', 'id']
exe_dir = 'exe/'
print(input_files_db)

credd = htcondor.Credd()
credd.add_user_cred(htcondor.CredTypes.Kerberos, None)


files = glob.glob(os.path.join(log_dir, '*'))
for f in files:
    os.remove(f)

for _, row in input_files_db.iterrows():#fileN, path in enumerate(input_files_db['path'].to_list()):

    lPath = row['path']
    total_events = row['nEvents']
    fid = row['id']

    job_template = {
        "executable": "start_FS.sh",      
        "arguments": f"{path_to_fs} $(input_file_name) $(start_event) $(nEvents) $(extra_fs_args)",          # we will pass in the value for this macro via itemdata
        "transfer_input_files": "$(input_file)",    # we also need HTCondor to move the file to the execute node
        "should_transfer_files": "yes",             # force HTCondor to transfer files even though we're running entirely inside a container (and it normally wouldn't need to)
        "output": os.path.join(log_dir, f"fs-{fid}-$(ProcId).out"),  
        "error": os.path.join(log_dir, f"fs-{fid}-$(ProcId).err"),  
        "log": os.path.join(log_dir, f"cat-{fid}-$(ProcId).log"),              
        "request_cpus": "1",
        'MY.SendCredential': True,
        'environment' :f'"out_dir={os.path.join(output_dir, run_tag, str(fid))}/$(subjob)"'# inputFile={lPath}"'#SHIP_CVMFS_SETUP_FILE=$ENV(SHIP_CVMFS_SETUP_FILE) FAIRSHIP_DIR=$ENV(FAIRSHIP) MAGNET_GEO=$ENV(MAGNET_GEO)"
             
    #    "request_memory": "4Gi",       
    #    "request_disk": "1Gi",           
    }

    iter_data = []#[{'input_file_name': str(path), 'subjob': str(subjob)} for subjob, path in enumerate(range(2))]
    for i in range(np.ceil(total_events / events_per_job).astype('int')):
        start_event = i * events_per_job
        nEvents = events_per_job if (start_event + events_per_job) <= total_events else (total_events - start_event)
        iter_data.append({'input_file_name':lPath, 'subjob': str(i), 'start_event': str(start_event), 'nEvents':str(nEvents), 'extra_fs_args': extra_fs_args})

    if debug:
        iter_data = iter_data[:2]
        iter_data[0]['nEvents'] = '10'
        iter_data[1]['nEvents'] = '10'

    schedd = htcondor.Schedd()
    cat_job = htcondor.Submit(job_template)
    # print(iter_data)
    submit_result = schedd.submit(cat_job, itemdata = iter(iter_data))  # submit one job for each item in the itemdata

    print(submit_result.cluster())

    if debug:
        break

def run_connmon(files, jobs_per_file=50, output=None):
    pass
def run_docker():
    pass


