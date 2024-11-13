# Hesiod Aria
Uses [Project Hesiod](https://github.com/boconnor2017/hesiod), a Photon based approach to deploy an immutable Aria environment on VCF. There are two goals with this project:

| Goal | Description |
|------|-------------|
| Fast and Autonomous Aria Environment | Using python, deploy the Aria Suite on an existing VCF environment. |
| Zero Touch Automation | Interact with JSON file only for lab specific configurations. The automation will do the rest. |


# Prerequisites
The following binaries are **required** to run hesiod-vcf-validation:

| Requirement | Description |
|-------------|-------------|
| PhotonOS OVA | version 5.0 recommended (download from [VMware GitHub](https://vmware.github.io/photon/)) |

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

## 