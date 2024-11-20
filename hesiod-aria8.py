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
    print("    TODO: Deploy Aria Suite Lifecycle Manager ova.")
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
    i=0
    while i < len(aslcm_session_return_json):
        err = "    Datacenter ID for "+aslcm_session_return_json[i]["dataCenterName"]+": "+aslcm_session_return_json[i]["dataCenterVmid"]
        liblog.write_to_logs(err, logfile_name)
        i=i+1

    # Add VCF Managment vCenter to ASLCM Datacenter
    err = "Adding Management vCenter "+env_json_py["vcf"]["management_vcenter"]["vcenter_name"]+"."
    liblog.write_to_logs(err, logfile_name)
    err = "    FQDN: "+env_json_py["vcf"]["management_vcenter"]["fqdn"]+"."
    liblog.write_to_logs(err, logfile_name)
    err = "    IP: "+env_json_py["vcf"]["management_vcenter"]["ip"]+"."
    liblog.write_to_logs(err, logfile_name)
    err = "    Username: "+env_json_py["vcf"]["management_vcenter"]["username"]+"."
    liblog.write_to_logs(err, logfile_name)
    err = "    Password: "+env_json_py["vcf"]["management_vcenter"]["password"]+"."
    liblog.write_to_logs(err, logfile_name)
    err = "    vCenter Used As: "+env_json_py["vcf"]["management_vcenter"]["vcenter_used_as"]+"."
    liblog.write_to_logs(err, logfile_name)
    err = "    Add vCenter to this Datacenter: "+aslcm_session_return_json[env_json_py["vcf"]["management_vcenter"]["add_to_this_aslcm_datacenter"]]["dataCenterName"]+"."
    liblog.write_to_logs(err, logfile_name)
    dc_vm_id = aslcm_session_return_json[env_json_py["vcf"]["management_vcenter"]["add_to_this_aslcm_datacenter"]]["dataCenterVmid"]
    err = "    Datacenter ID: ("+aslcm_session_return_json[env_json_py["vcf"]["management_vcenter"]["add_to_this_aslcm_datacenter"]]["dataCenterName"]+") "+dc_vm_id
    liblog.write_to_logs(err, logfile_name)
    aslcm_session_return_code = arialib.add_vcenter_to_aslcm_datacenter(aslcm_token, env_json_py["aria"]["lifecycle_manager"]["fqdn"], env_json_py["vcf"]["management_vcenter"]["vcenter_name"], env_json_py["vcf"]["management_vcenter"]["fqdn"], env_json_py["vcf"]["management_vcenter"]["username"], env_json_py["vcf"]["management_vcenter"]["password"], env_json_py["vcf"]["management_vcenter"]["vcenter_used_as"], dc_vm_id)
    err = "Return: "+str(aslcm_session_return_code)
    liblog.write_to_logs(err, logfile_name)

    # Get Available Product Versions
    err = "Getting available product versions."
    liblog.write_to_logs(err, logfile_name)
    i=0
    while i < len(env_json_py["products"]):
        err = "    ID: "+env_json_py["products"][i]["id"]+" ("+env_json_py["products"][i]["name"]+")"
        liblog.write_to_logs(err, logfile_name)
        aslcm_session_return_json, aslcm_session_return_code = arialib.get_aslcm_product_versions(aslcm_token, env_json_py["aria"]["lifecycle_manager"]["fqdn"], env_json_py["products"][i]["id"])
        err = "    Return: "+str(aslcm_session_return_code)
        liblog.write_to_logs(err, logfile_name)
        product_versions = libjson.dump_json(aslcm_session_return_json)
        err = "    Available Product Versions: "+product_versions
        liblog.write_to_logs(err, logfile_name)
        i=i+1
    

_main_()
