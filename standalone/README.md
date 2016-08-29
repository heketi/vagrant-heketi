# Standalone Heketi Demo

This vagrant-ansible script creates a setup for Heketi to manage GlusterFS.  It creates four VMs (storage0,storage1,storage2,storage3) with eight 500 GB drives each.  The ansible script only installs gluster-server on each of the storage servers and then enables the gluster service.  It does not create or initialize any of the disks.  The disks will later be managed by Heketi.  The script also creates a client VM to demo mounting the volume created by Heketi.

# Requisites

* You will need Virtualbox or libvirt, Vagrant, and Ansible installed on your system.
* Virtualbox must have a host network interface ip of 192.168.10.1

# Setup

* For Virtualbox type: `./up.sh`
* For Libvirt type: `sudo ./up.sh --provider=libvirt`

* Now load the topology

```
$ <sudo for libvirt> vagrant ssh storage0
$ export HEKETI_CLI_SERVER=http://localhost:8080
$ heketi-cli topology load --json=topology_<provider>.json
```

Where _provider_ is either `virtualbox` or `libvirt` depending on the vagrant provider.

# Create a volume
Heketi REST API has been created to be consumed by services like OpenStack Manila, Kubernetes, OpenShift, and others.  For simplicity, a command line tool has been provided for use.

To create a 100GiB Replica 3 volume execute the following:

```
$ heketi-cli volume create --size=100
```

# More information
* See the command line help screen by typing: `./heketi-cli -h`
* Please see the [API](https://github.com/heketi/heketi/wiki/API) for REST commands.
