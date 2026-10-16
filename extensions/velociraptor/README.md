# Velociraptor extension

This extension adds a dedicated Linux Velociraptor server at
`<ip_range>.53` and installs a deployment-specific Velociraptor client MSI on
every Windows host in the Ansible `domain` group.

The server GUI and SSH service accept traffic only from the jump box that ran
the provisioning playbook. The client frontend on TCP 8000 accepts traffic
only from the managed Windows hosts. See the
[operator guide](../../docs/mkdocs/docs/extensions/velociraptor.md) for access,
credentials, firewall rules, and troubleshooting.

```text
install_extension velociraptor
```
