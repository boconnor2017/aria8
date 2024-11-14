# General imports
import base64 
import requests

# vSphere Automation Python SDK Imports
from vmware.vapi.vsphere.client import create_vsphere_client

# Aria Suite Lifecycle Manager Functions
def authenticate_to_aslcm(aslcm_user, aslcm_pw, aslcm_fqdn):
    aslcm_token = get_aslcm_auth_token(aslcm_user, aslcm_pw)
    #Syntax: curl -H "Authorization: Basic <token>" -k https://<LCM_hostname>/lcm/lcops/api/settings/systemsettings
    #aslcm_session = requests.Session()
    aslcm_session = requests.get("https://"+aslcm_fqdn+"/lcm/lcops/api/settings/systemsettings", headers={"Authorization": "Basic "+aslcm_token}, verify=False)
    aslcm_session_return_code = (aslcm_session.status_code)
    return aslcm_session, aslcm_session_return_code

def get_aslcm_auth_token(aslcm_user, aslcm_pw):
    aslcm_token_b64 = base64.b64encode(bytes(aslcm_user+":"+aslcm_pw, 'utf-8'))
    aslcm_token = aslcm_token_b64.decode('utf-8')
    #aslcm_token = "b\'"+aslcm_token+"\'"
    return aslcm_token

# vSphere Automation Python SDK Functions
def connect_to_vcenter(vcenter_ip, vcenter_username, vcenter_password, session):
    vsphere_client = create_vsphere_client(server=vcenter_ip, username=vcenter_username, password=vcenter_password, session=session)
    return vsphere_client

def list_vms_from_vcenter(vsphere_client):
    vm_list = vsphere_client.vcenter.VM.list()
    return vm_list

