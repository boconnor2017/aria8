# vSphere Automation Python SDK Imports
import requests
import urllib3
from vmware.vapi.vsphere.client import create_vsphere_client
session = requests.session()
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# vSphere Python SDK Functions
def connect_to_vcenter(vcenter_ip, vcenter_username, vcenter_password, session):
    vsphere_client = create_vsphere_client(server=vcenter_ip, username=vcenter_username, password=vcenter_password, session=session)
    return vsphere_client

def list_vms_from_vcenter(vsphere_client):
    vm_list = vsphere_client.vcenter.VM.list()
    return vm_list