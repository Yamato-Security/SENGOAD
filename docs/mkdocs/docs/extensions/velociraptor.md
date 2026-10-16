# Velociraptor

The `velociraptor` extension adds a dedicated Ubuntu server and remotely
installs the Velociraptor client service on every Windows host in the lab's
`domain` inventory group. This includes Windows extensions such as `ws01` or
`exchange` when they are enabled on the same instance.

## Install

For Ludus, prepare the Ubuntu template first:

```text
ludus templates add -d ubuntu-22.04-x64-server
ludus templates build
```

From the SENGOAD console:

```text
install_extension velociraptor
```

The extension downloads pinned Velociraptor release artifacts, verifies their
SHA-256 hashes, generates a unique deployment PKI, repacks the official Windows
MSI with the generated client configuration, and installs that MSI on all
Windows targets. Provisioning can be run again safely; the deployment PKI and
administrator password are not regenerated.

## Network location and ports

If the instance range is `192.168.56.0/24`, the server is
`192.168.56.53`. In general, replace the last octet of the instance range with
`.53`.

| Purpose | Address | Access policy |
| --- | --- | --- |
| Client frontend | `https://<ip_range>.53:8000/` | Each managed Windows IP only |
| Admin GUI | `https://<ip_range>.53:8889/` | Provisioning/Kali jump box only |
| SSH | `<ip_range>.53:22` | Provisioning/Kali jump box only |

UFW denies every other inbound connection. The GUI also applies its own CIDR
allowlist, independent of UFW. The allowed management IP is detected from the
SSH connection that runs Ansible, which is the Kali jump box at
`<ip_range>.100` for the Azure deployment. This also keeps the extension usable
with the other providers' provisioning jump boxes.

## Open the GUI through the jump box

Do not expose TCP 8889 publicly. Forward it through the jump box instead. For
AWS and Azure, obtain the public jump-box address and key from the SENGOAD
instance workspace, then run this on the operator workstation:

```bash
ssh -N \
  -L 8889:<ip_range>.53:8889 \
  -i workspace/<instance_id>/ssh_keys/ubuntu-jumpbox.pem \
  goad@<jumpbox_public_ip>
```

Open `https://127.0.0.1:8889/` and accept the warning for the
deployment-specific self-signed certificate. The GUI username is `admin`.

## Retrieve the GUI password

The password is randomly generated on first provision and stored only on the
Velociraptor server at `/root/velociraptor-admin-password`. First enter the
jump box with the `ssh_jumpbox` console command. Then SSH from the jump box to
`<ip_range>.53` and read it:

```bash
sudo cat /root/velociraptor-admin-password
```

The server account depends on the provider:

| Provider | Server account and connection |
| --- | --- |
| AWS | `goadmin`; use the instance's `ubuntu-jumpbox.pem` because the jump box key is authorized on Linux VMs |
| Azure | `goadmin`; use the instance's `velociraptor_ssh.pem` |
| VirtualBox/VMware/ESXi | `vagrant`; connect from the provisioning VM or other host that ran Ansible |
| Ludus | `localuser`; connect from the Ludus router/jump host |
| Proxmox | Use the SSH account configured in the Ubuntu template |

For example, on Azure after entering the Kali jump box:

```bash
chmod 600 ~/GOAD/workspace/<instance_id>/ssh_keys/velociraptor_ssh.pem
ssh -i ~/GOAD/workspace/<instance_id>/ssh_keys/velociraptor_ssh.pem \
  goadmin@<ip_range>.53
sudo cat /root/velociraptor-admin-password
```

Keep this password and `/etc/velociraptor/server.config.yaml` private. The
server configuration contains the deployment CA private key, and replacing it
would break trust with all enrolled clients.

## Verify the deployment

On a Windows target:

```powershell
Get-Service Velociraptor
Test-NetConnection <ip_range>.53 -Port 8000
```

On the server:

```bash
sudo systemctl status velociraptor_server
sudo ufw status verbose
```

Clients enroll automatically on their first connection and then appear in the
Velociraptor GUI. The MSI is removed from each Windows staging directory after
installation.
