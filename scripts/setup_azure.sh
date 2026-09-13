#!/bin/bash

# Install git and python3
sudo apt-get update
sudo apt-get install -y git python3-venv python3-pip sshpass rsync

# Install the standard Kali pentest toolset (nmap, impacket, netexec, bloodhound-python, hashcat, etc.)
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y kali-linux-default

#python3 -m venv .venv
#source .venv/bin/activate

# Install ansible and pywinrm
# --break-system-packages: Kali's Python enforces PEP 668 (externally-managed-environment)
python3 -m pip install --upgrade pip --break-system-packages
# ansible-core 2.12.6 does not support Python >= 3.11 (Kali ships 3.13); match requirements_311.yml's pin
python3 -m pip install ansible-core==2.18.0 --break-system-packages
python3 -m pip install pywinrm --break-system-packages

# Install the required ansible libraries
/home/goad/.local/bin/ansible-galaxy install -r /home/goad/GOAD/ansible/requirements.yml

# set color
sudo sed -i '/force_color_prompt=yes/s/^#//g' /home/*/.bashrc
sudo sed -i '/force_color_prompt=yes/s/^#//g' /root/.bashrc