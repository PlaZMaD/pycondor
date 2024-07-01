import htcondor
import classad
import pandas as pd
import os

output_dir = '/eos/experiment/ship/user/ekurbato/condor_output/'
log_dir = "/eos/experiment/ship/user/ekurbato/condor/logs"
subdir = 'test_run'
output_dir = os.path.join(output_dir, subdir)
input_files_db = pd.read_csv('input_for_muon_prod.txt', header=None)
input_files_db.columns=['path', 'nEvents', 'id']
exe_dir = 'exe/'
print(input_files_db)


job_template = {
    "executable": "test.sh",      
    "arguments": "$(input_file_name)",          # we will pass in the value for this macro via itemdata
    "transfer_input_files": "$(input_file)",    # we also need HTCondor to move the file to the execute node
    "should_transfer_files": "yes",             # force HTCondor to transfer files even though we're running entirely inside a container (and it normally wouldn't need to)
    "output": os.path.join(log_dir, "fs-$(ProcId).out"),  
    "error": os.path.join(log_dir, "fs-$(ProcId).err"),  
    "log": os.path.join(log_dir, "cat-$(ProcId).log"),              
    "request_cpus": "1",             
#    "request_memory": "4Gi",       
#    "request_disk": "1Gi",           
}

iter_data = [{'input_file_name': path} for path in input_files_db['path'].to_list()]
schedd = htcondor.Schedd()
cat_job = htcondor.Submit(job_template)
submit_result = schedd.submit(cat_job, itemdata = iter(iter_data))  # submit one job for each item in the itemdata

print(submit_result.cluster())

def run_connmon(files, jobs_per_file=50, output=None):
    pass
def run_docker():
    pass


