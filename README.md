# Heketi Demo
This vagrant-ansible script creates a setup for Heketi to manage GlusterFS.  It creates four VMs (storage0,storage1,storage2,storage3) with eight 500 GB drives each.  The ansible script only installs gluster-server on each of the storage servers and then enables the gluster service.  It does not create or initilize any of the disks.  The disks will later be managed by Heketi.  The script also creates a client VM to demo mounting the volume created by Heketi.

# Requisites
* You will need Virtualbox, Vagrant, and Ansible installed on your system.
* Virtualbox must have a host network interface ip of 192.168.10.1
* Must have Firefox RESTclient installed
    * Go to _Add-ons_ on the Firefox menu
    * Search and install RESTclient

# Setup
* Type: `./up.sh` to create cluster
* Start up heketi:

```
$ vagrant ssh storage0
$ ./heketi &
$ exit
```

* In the Firefox RESTclient, choose _GET_ in the method and type `http://192.168.10.100:8080/nodes` in the URL.  It should return

```
{"nodes":[]}
```

# Demo

## Setting up the cluster topology
First thing you need to do is tell Heketi about the cluster.  You will tell Heketi which nodes and which drives to use.

> NOTE: All of the following commands refer to the Firefox RESTclient.

* You will need to register each storage nodes:
    * storage0 - 192.168.10.100
    * storage1 - 192.168.10.101
    * storage2 - 192.168.10.102
    * storage3 - 192.168.10.103

1. Method: _POST_ URL: `http://192.168.10.100:8080/nodes`
1. In the *Body* copy and paste the following:

```
{ "name" : "<type the one of the ip address here from the ip addresses above>", "zone": "1" }
```

For example:

```
{ "name" : "192.168.10.100", "zone": "1" }
```

> NOTE: Zone is refers to failure domains.

* In the _Response Body (Highlight)_ notice the _id_.  Copy the id to the clipboard.

Now we will add devices Heketi can use on this node:

* Method: _POST_ URL: `http://192.168.10.100:8080/nodes/<paste id>/devices`
* In the body, you will tell Heketi which drives to use.  Copy and paste the following to the *Body*

```
{ "devices": [ { "name" : "/dev/sdb", "weight" : 100 }, { "name" : "/dev/sdc", "weight" : 100 }, { "name" : "/dev/sdd", "weight" : 100 }, { "name" : "/dev/sde", "weight" : 100 }, { "name" : "/dev/sdf", "weight" : 100 }, { "name" : "/dev/sdg", "weight" : 100 }, { "name" : "/dev/sdh", "weight" : 100 }, { "name" : "/dev/sdi", "weight" : 100 } ] }
```

> NOTE: _Weight_ is the relative weight of the device in comparison to other devices.  For more inforation please read [OpenStack Swift's Ring Documentation](http://docs.openstack.org/developer/swift/overview_ring.html#list-of-devices)

* Notice the status code of `201 Created` in the _Response Headers_ tab.  Here Heketi went into the system and initialized the disks to be managed by LVM.

* Now repeat for the other IP addresses.

Once you have finished, you can view the cluster by doing the following:

* Method: _GET_  URL: `http://192.168.10.100:8080/nodes`


## Create a volume

Now we let Heketi determine where to place the bricks and create our volume.

> NOTE: Heketi uses OpenStack Swift's Ring algorithm to determine the object, I mean, brick placements in the cluster.

* Method: _POST_  URL: `http://192.168.10.100:8080/volumes`
* Type the following in the *Body*

```
{ "size" : 1000000000, "replica": 2 }
```

> NOTE: Size is in KB.  If replica is omitted then it will default to `2`.  You can also add `"name" : "myvolumename"` if you want to specify a name.

* In the _Response Body (Hightlight)_ you will notice the `mount`.  Copy the mount information.

If you miss the information, you can see it again by typing:

* Method: _GET_  URL: `http://192.168.10.100:8080/volumes`

Notice that storage has been borrowed from the cluster by looking at the devices in:

* Method: _GET_  URL: `http://192.168.10.100:8080/nodes`

## Mounting the volume

Now we ssh into the `client` VM and mount the volume:

```
$ vagrant ssh client
$ sudo mkdir /gluster
$ sudo mount -t glusterfs  <mount from from above> /gluster
```

## Delete the volume

Go to the client and umount the volume:

```
$ vagrant ssh client
$ sudo umount /gluster
```

Get the _id_ of the volume to delete:

* Method: _GET_  URL: `http://192.168.10.100:8080/volumes`

Notice the _id_ in the _Request Body (Highlight)_. Copy the id

Delete the volume by using the following command:

* Method: _DELETE_ URL: `http://192.168.10.100:8080/volumes/<id of volume>`

Notice that the storage has been returned to the cluster by looking at the devices in:

* Method: _GET_  URL: `http://192.168.10.100:8080/nodes`


 
