# GlusterFS converged with OpenShift Demo

This vagrant-ansible script creates a setup for Heketi to manage containerized GlusterFS deployed in OpenShift.  It creates five VMs (client, master, atomic0, atomic1, atomic2) with three drives each.  The ansible script only installs OpenShift on the master and atomic systems, then deploys GlusterFS containers and Heketi into the cluster.

# Requisites

* You will need libvirt, Vagrant, and Ansible installed on your system.
* 12 GB of RAM or more

# Setup

* For Libvirt type: `sudo ./up.sh --provider=libvirt`
Note: For all subsequent operations, use vagrant commands like `vagrant halt` and
`vagrant up` instead of `up.sh`. The provisioner is not idempotent.

* Log into the client and get the status of the cluster

```
$ sudo vagrant ssh client
[vagrant@client]$ oc status
```

# Usage
Now you can setup an application to use the storage:

Follow the [Usage Example](https://github.com/heketi/heketi/wiki/OpenShift-Integration---Project-Aplo#usage-example)

