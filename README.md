# Hesiod Aria
Uses [Project Hesiod](https://github.com/boconnor2017/hesiod), a Photon based approach to deploy an immutable Aria environment on VCF. There are two goals with this project:

| Goal | Description |
|------|-------------|
| Fast and Autonomous Aria Environment | Using python, deploy the Aria Suite on an existing VCF environment. |
| Zero Touch Automation | Interact with JSON file only for lab specific configurations. The automation will do the rest. |


# Prerequisites
The following binaries are **required** to run `hesiod-aria8.py`:

| Requirement | Description |
|-------------|-------------|
| PhotonOS OVA | version 5.0 recommended (download from [VMware GitHub](https://vmware.github.io/photon/)) |

The following infrastructure is **required** to run `hesiod-aria8.py`:

| Requirement | Description |
|-------------|-------------|
| DNS Server  | recommended: use [hesiod-dns](https://github.com/boconnor2017/hesiod-dns) to spin up an immutable DNS server and configure necessary DNS entries for VCF |
| VMware Cloud Foundation Management Domain | version 5.2 recommended (AVN is optional), nested is supported (if using nested, its recommended to use [hesiod-vcf5](https://github.com/boconnor2017/hesiod-vcf5)) |
| Aria Suite Lifecycle Manager | version 8.18 must be deployed |

The following binaries are recommended to run `hesiod-aria8.py` (binaries must be uploaded to the Aria Suite Lifecycle Manager `/data/drop/` folder):

| Lab Use Case | Description | Required Binaries |
|--------------|-------------|-------------------|
| Service Automation | IaaS, PaaS, XaaS | VMware Identity Manager (Workspace ONE) and Aria Automation 8.x |
| Telemetry | Monitoring, Alerting, Logging | Aria Operations and Aria Operations for Logs |
| Private Cloud | All of the above |

# Quick Start
Deploy Photon OS OVA to the physical server. Follow the steps in the [Hesiod Photon OS Quick Start](https://github.com/boconnor2017/hesiod/blob/main/photon/readme.md) readme file to prep the Photon server for this project. 

*Recommended: run these scripts as root.*
```
cd /usr/local/
```
```
git clone https://github.com/boconnor2017/hesiod-aria8
```
```
cp -r hesiod/python/ hesiod-aria8/hesiod
```
```
mkdir hesiod-aria8/photon/
```
```
cp -r hesiod/photon/install_vsphere_py_sdk.sh hesiod-aria8/photon
```
```
cp -r hesiod/photon/install_pyvmomi.sh hesiod-aria8/photon
```
```
cd hesiod-aria8
```
```
sh photon/install_vsphere_py_sdk.sh
```
```
sh photon/install_vsphere_py_sdk.sh sh photon/install_pyvmomi.sh
```

## Step 1: Edit the JSON Configuration 
Populate the variables in `json/lab_environment.json`. The automation will use these values to connect to your existing VCF environment using your existing Aria Suite Lifecycle Manager API. 

## Step 2: Deploy Aria
```
python3 hesiod-aria8.py
```