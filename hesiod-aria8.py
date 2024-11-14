# Import Hesiod libraries
from hesiod import lib_general as libgen
from hesiod import lib_json as libjson
from hesiod import lib_logs_and_headers as liblog 
from hesiod import lib_paramiko as libpko 

# Import Aria libraries
from lib import aria as arialib

# Import Standard Python libraries
import os
import sys
import requests
import urllib3
session = requests.session()
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Import json configuration parameters
env_json_str = libjson.populate_var_from_json_file("json", "lab_environment.json")
env_json_py = libjson.load_json_variable(env_json_str)
this_script_name = os.path.basename(__file__)
logfile_name = env_json_py["logs"][this_script_name]

# Hesiod Header and Log init
liblog.hesiod_print_header()
liblog.hesiod_log_header(logfile_name)
err = "Successfully imported Hesiod python libraries."
liblog.write_to_logs(err, logfile_name)
err = "Succesfully initialized logs to "+logfile_name
liblog.write_to_logs(err, logfile_name)
err = ""
liblog.write_to_logs(err, logfile_name)

# Local Functions
def _main_():
    # CLI Message
    print("Deploying Aria Suite.")

    # Connect to Management vCenter using JSON config params
    err = "Connecting to vCenter: IP="+env_json_py["vcf"]["management_vcenter"]["ip"]+", UN="+env_json_py["vcf"]["management_vcenter"]["username"]+", "+env_json_py["vcf"]["management_vcenter"]["password"]
    liblog.write_to_logs(err, logfile_name)
    vsphere_client = arialib.connect_to_vcenter(env_json_py["vcf"]["management_vcenter"]["ip"], env_json_py["vcf"]["management_vcenter"]["username"], env_json_py["vcf"]["management_vcenter"]["password"], session)
    err = "Getting VM List."
    liblog.write_to_logs(err, logfile_name)
    vm_list = arialib.list_vms_from_vcenter(vsphere_client)
    vm_count = len(vm_list)
    err = "VM Count: "+str(vm_count)
    liblog.write_to_logs(err, logfile_name)

    # Deploy Aria Suite Lifecycle Manager and Get Token
    print("    TODO: Deploy Aria Suite Lifecycle Manager.")
    err = "Connecting to Aria Suite LCM. FQDN: "+env_json_py["aria"]["lifecycle_manager"]["fqdn"]
    liblog.write_to_logs(err, logfile_name)
    aslcm_token, aslcm_session_return_code = arialib.authenticate_to_aslcm(env_json_py["aria"]["lifecycle_manager"]["username"], env_json_py["aria"]["lifecycle_manager"]["password"], env_json_py["aria"]["lifecycle_manager"]["fqdn"])
    err = "Return: "+str(aslcm_session_return_code)
    liblog.write_to_logs(err, logfile_name)
    err = "Auth Token: "+aslcm_token
    liblog.write_to_logs(err, logfile_name)

    # Create Passwords in ASLCM Password Locker
    err = "Creating ASLCM users for password locker. Count: "+str(len(env_json_py["aria"]["lifecycle_manager_users_for_locker"]))
    liblog.write_to_logs(err, logfile_name)
    i=0
    while i < len(env_json_py["aria"]["lifecycle_manager_users_for_locker"]):
        err = "    User "+str(i+1)+": "+env_json_py["aria"]["lifecycle_manager_users_for_locker"][i]["username"]+"/"+env_json_py["aria"]["lifecycle_manager_users_for_locker"][i]["password"]
        liblog.write_to_logs(err, logfile_name)
        aslcm_session_return_code = arialib.create_aslcm_locker_users(aslcm_token, env_json_py["aria"]["lifecycle_manager"]["fqdn"], env_json_py["aria"]["lifecycle_manager_users_for_locker"][i]["password"], env_json_py["aria"]["lifecycle_manager_users_for_locker"][i]["username"])
        err = "Return: "+str(aslcm_session_return_code)
        liblog.write_to_logs(err, logfile_name)
        i=i+1

    # Create Datacenter
    err = "Creating ASLCM datacenters. Count: "+str(len(env_json_py["aria"]["lifecycle_manager_datacenters"]))
    liblog.write_to_logs(err, logfile_name)
    i=0
    while i < len(env_json_py["aria"]["lifecycle_manager_datacenters"]):
        err = "    Datacenter "+str(i+1)+": "+env_json_py["aria"]["lifecycle_manager_datacenters"][i]["name"]+"/"+env_json_py["aria"]["lifecycle_manager_datacenters"][i]["location"]
        liblog.write_to_logs(err, logfile_name)
        aslcm_session_return_code = arialib.create_aslcm_data_center(aslcm_token, env_json_py["aria"]["lifecycle_manager"]["fqdn"], env_json_py["aria"]["lifecycle_manager_datacenters"][i]["name"], env_json_py["aria"]["lifecycle_manager_datacenters"][i]["location"])
        err = "Return: "+str(aslcm_session_return_code)
        liblog.write_to_logs(err, logfile_name)
        i=i+1

    # Get config details from created datacenters
    err = "VALIDATE: Getting ASLCM configured datacenters."
    liblog.write_to_logs(err, logfile_name)
    aslcm_session_return_json, aslcm_session_return_code = arialib.get_aslcm_datacenters(aslcm_token, env_json_py["aria"]["lifecycle_manager"]["fqdn"])
    err = "Return: "+str(aslcm_session_return_code)
    liblog.write_to_logs(err, logfile_name)
    err = str(aslcm_session_return_json)
    liblog.write_to_logs(err, logfile_name)

_main_()