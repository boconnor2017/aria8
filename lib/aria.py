# General imports
import base64 
import requests

# vSphere Automation Python SDK Imports
from vmware.vapi.vsphere.client import create_vsphere_client

# Aria Suite Lifecycle Manager Functions
def authenticate_to_aslcm(aslcm_user, aslcm_pw, aslcm_fqdn):
    aslcm_token = get_aslcm_auth_token(aslcm_user, aslcm_pw)
    #Syntax: curl -H "Authorization: Basic <token>" -k https://<LCM_hostname>/lcm/lcops/api/settings/systemsettings
    aslcm_session = requests.get("https://"+aslcm_fqdn+"/lcm/lcops/api/settings/systemsettings", headers={"Authorization": "Basic "+aslcm_token}, verify=False)
    aslcm_session_return_code = (aslcm_session.status_code)
    return aslcm_token, aslcm_session_return_code

def add_license_key_to_aslcm_locker(aslcm_token, aslcm_fqdn, license_alias, license_key):
    #Syntax: curl -k -X POST 'https://hesvcf-aria01.hesiod.local/lcm/locker/api/v2/license/validate-and-add' -H 'Accept: application/json' -H 'Authorization: Basic YWRtaW5AbG9jYWw6Vk13YXJlMTIzIVZNd2FyZTEyMyE=' -H 'Content-Type: application/json' -d '{"alias": "license1", "serialKey": "AB0DC-EF280-48JH1-00024-1JK"}'
    # /lcm/locker/api/v2/license/validate-and-add
    req_headers = {"Accept": "application/json", "Authorization": "Basic "+aslcm_token, "Content-Type": "application/json"}
    req_data = {
        "alias": license_alias, 
        "serialKey": license_key
    }
    aslcm_session = requests.post("https://"+aslcm_fqdn+"/lcm/locker/api/v2/license/validate-and-add", headers=req_headers, json=req_data, verify=False)
    aslcm_session_return_code = (aslcm_session.status_code)
    aslcm_session_return_json = (aslcm_session.json())
    return aslcm_session_return_json, aslcm_session_return_code

def add_vcenter_to_aslcm_datacenter(aslcm_token, aslcm_fqdn, vcenter_name, vcenter_fqdn, vcenter_username, vcenter_password, vcenter_used_as, dc_vm_id):
    #Syntax: curl -k -X POST '$url/lcm/lcops/api/v2/datacenters/$dataCenterVMid/vcenters' -H 'Accept: application/json' -H 'Authorization: Basic YWRtaW5AbG9jYWw6VGhpc0lzUGFzc3dvcmQ=' -H 'Content-Type: application/json' -d '{"vCenterName": "VC1","vCenterHost": "lcm-vc2.sqa.local","vcUsername": "administrator@vsphere.local","vcPassword": "MyExamplePassword","vcUsedAs": "MANAGEMENT"}'
    req_headers = {"Accept": "application/json", "Authorization": "Basic "+aslcm_token, "Content-Type": "application/json"}
    req_data = {
        "vCenterName": vcenter_name,
        "vCenterHost": vcenter_fqdn,
        "vcUsername": vcenter_username,
        "vcPassword": vcenter_password,
        "vcUsedAs": vcenter_used_as
    }
    aslcm_session = requests.post("https://"+aslcm_fqdn+"/lcm/lcops/api/v2/datacenters/"+dc_vm_id+"/vcenters", headers=req_headers, json=req_data, verify=False)
    aslcm_session_return_code = (aslcm_session.status_code)
    return aslcm_session_return_code

def create_aslcm_data_center(aslcm_token, aslcm_fqdn, datacenter_name, datacenter_location):
    #Syntax: curl -X POST '$url/lcm/lcops/api/v2/datacenters' -H 'Authorization: Basic <token>' -H 'Content-Type: application/json' -d '{"dataCenterName": "BLR","primaryLocation": "Bangalore; Karnataka;IN;12.97194;77.59369"}' 
    req_headers = {"Accept": "application/json", "Authorization": "Basic "+aslcm_token, "Content-Type": "application/json"}
    req_data = {
        "dataCenterName": datacenter_name, 
        "primaryLocation": datacenter_location
    }
    aslcm_session = requests.post("https://"+aslcm_fqdn+"/lcm/lcops/api/v2/datacenters", headers=req_headers, json=req_data, verify=False)
    aslcm_session_return_code = (aslcm_session.status_code)
    return aslcm_session_return_code

def create_aslsm_environment(aslcm_token, aslcm_fqdn):
    #Syntax: /lcm/lcops/api/v2/environments
    req_url = generate_api_post_url("/lcm/lcops/api/v2/environments", aslcm_fqdn)
    req_headers={"Accept": "application/json", "Authorization": "Basic "+aslcm_token, "Content-Type": "application/json"}
    req_data={

    }

def create_aslcm_locker_users(aslcm_token, aslcm_fqdn, new_password, new_username):
    #Syntax: curl -k -X POST '$url/lcm/locker/api/v2/passwords' -H 'Authorization: Basic <token>' -H 'Content-Type: application/json' -d '{"alias": "VC-password", "password": "ExampleLockerPassword", "passwordDescription": "", "principal": "", "transactionId": "", "userName": ""}'
    req_headers={"Accept": "application/json", "Authorization": "Basic "+aslcm_token, "Content-Type": "application/json"}
    req_data={
        "alias": "VC-password", 
        "password": new_password, 
        "passwordDescription": "Hesiod Aria 8 Password Generated", 
        "principal": "", 
        "transactionId": "", 
        "userName": new_username
    }
    aslcm_session = requests.post("https://"+aslcm_fqdn+"/lcm/locker/api/v2/passwords", headers=req_headers, json=req_data, verify=False)
    aslcm_session_return_code = (aslcm_session.status_code)
    return aslcm_session_return_code

def generate_aslcm_certificate(aslcm_token, aslcm_fqdn, cert_name, cert_common_name, cert_organization, cert_org_unit, cert_country_code, cert_locality, cert_state, cert_key_length, cert_hostnames, cert_ips ):
    #Syntax: curl -X POST '$url/lcm/locker/api/v2/certificates' -H 'Accept: application/json' -H 'Authorization: Basic YWRtaW5AbG9jYWw6VGhpc0lzUGFzc3dvcmQ=' -H 'Content-Type: application/json' -d '{ "alias": "cert2", "c": "certificate2", "cN": "certificate2", "ip": ["10.196.15.13"], "host": ["*.sqa.local"], "cN": "vmware", "oU": "vmware", "size": "2048", "o": "vmware", "l": "IN", "sT": "IN", "c": "IN"}'
    req_headers={"Accept": "application/json", "Authorization": "Basic "+aslcm_token, "Content-Type": "application/json"}
    req_data={
        "alias": cert_name, 
        "cN": cert_common_name, 
        "ip": cert_ips, 
        "host": cert_hostnames,
        "oU": cert_org_unit, 
        "size": cert_key_length, 
        "o": cert_organization, 
        "l": cert_locality, 
        "sT": cert_state, 
        "c": cert_country_code
    }
    aslcm_session = requests.post("https://"+aslcm_fqdn+"/lcm/locker/api/v2/certificates", headers=req_headers, json=req_data, verify=False)
    aslcm_session_return_code = (aslcm_session.status_code)
    return aslcm_session_return_code
 

def get_aslcm_auth_token(aslcm_user, aslcm_pw):
    aslcm_token_b64 = base64.b64encode(bytes(aslcm_user+":"+aslcm_pw, 'utf-8'))
    aslcm_token = aslcm_token_b64.decode('utf-8')
    #aslcm_token = "b\'"+aslcm_token+"\'"
    return aslcm_token

def get_aslcm_datacenters(aslcm_token, aslcm_fqdn):
    #Syntax: curl -X GET '$url/lcm/lcops/api/v2/datacenters' -H 'Accept: application/json' -H 'Authorization: Basic <token>'
    aslcm_session = requests.get("https://"+aslcm_fqdn+"/lcm/lcops/api/v2/datacenters", headers={"Authorization": "Basic "+aslcm_token, "Accept": "application/json"}, verify=False)
    aslcm_session_return_code = (aslcm_session.status_code)
    aslcm_session_return_json = (aslcm_session.json())
    return aslcm_session_return_json, aslcm_session_return_code

def get_aslcm_product_versions(aslcm_token, aslcm_fqdn, product_id):
    #Syntax: curl -k -X GET '$url/lcm/lcops/api/v2/policy/products/{productId}/versions' -H 'Authorization: Basic YWRtaW5AbG9jYWw6VGhpc0lzUGFzc3dvcmQ=' -H 'Accept: application/json'
    aslcm_session = requests.get("https://"+aslcm_fqdn+"/lcm/lcops/api/v2/policy/products/"+product_id+"/versions", headers={"Authorization": "Basic "+aslcm_token, "Accept": "application/json"}, verify=False)
    aslcm_session_return_code = (aslcm_session.status_code)
    aslcm_session_return_json = (aslcm_session.json())
    return aslcm_session_return_json, aslcm_session_return_code

def get_status_of_aslcm_request(aslcm_token, aslcm_fqdn, request_id):
    #Syntax: curl -X GET '$url /lcm/request/api/v2/requests/$requestId' -H 'Authorization: Basic YWRtaW5AbG9jYWw6VGhpc0lzUGFzc3dvcmQ=' 
    req_headers = {"Authorization": "Basic "+aslcm_token}
    aslcm_session = requests.get("https://"+aslcm_fqdn+"/lcm/request/api/v2/requests/"+request_id, headers=req_headers)
    aslcm_session_return_code = (aslcm_session.status_code)
    aslcm_session_return_json = (aslcm_session.json())
    return aslcm_session_return_json, aslcm_session_return_code

# vSphere Automation Python SDK Functions
def connect_to_vcenter(vcenter_ip, vcenter_username, vcenter_password, session):
    vsphere_client = create_vsphere_client(server=vcenter_ip, username=vcenter_username, password=vcenter_password, session=session)
    return vsphere_client

def list_vms_from_vcenter(vsphere_client):
    vm_list = vsphere_client.vcenter.VM.list()
    return vm_list

# Custom Functions
def generate_api_post_url(api_url, fqdn):
    #Syntax: copy path from swagger - example: /lcm/lcops/api/v2/environments
    #This script will create the necessary url for requests.post(url)
    req_url = "https://"+fqdn+api_url
    return req_url