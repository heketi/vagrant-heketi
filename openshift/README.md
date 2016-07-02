# GlusterFS converged with OpenShift Demo

This vagrant-ansible script creates an setup for Heketi to manage containerized GlusterFS deployed in OpenShift.  It creates four VMs (client, master, atomic0, atomi1, atomic2) with three drives each.  The ansible script only installs OpenShift on the master and atomic systems, then deploys GlusterFS containers and Heketi into the cluster.

# Requisites

* You will need libvirt, Vagrant, and Ansible installed on your system.
* 12 MG of RAM of more

# Setup

* For Libvirt type: `sudo ./up.sh --provider=libvirt`

* Now load the topology

```
$ sudo vagrant ssh storage0
$ export HEKETI_CLI_SERVER=http://heketi-default.cloudapps.example.com
```

# Usage
Heketi REST API has been created to be consumed by services like OpenStack Manila, Kubernetes, OpenShift, and others.  For simplicity, a command line tool has been provided for use.

Follow the [Usage Example](https://github.com/heketi/heketi/wiki/OpenShift-Integration---Project-Aplo#usage-example)

# More information
* See the command line help screen by typing: `./heketi-cli -h`
* Please see the [API](https://github.com/heketi/heketi/wiki/API) for REST commands.
