# -*- mode: ruby -*-
# vi: set ft=ruby :
#

NODES = 4
DISKS = 8

Vagrant.configure("2") do |config|
    config.vm.box = "chef/centos-7.1"
    config.ssh.insert_key = false

    # Make the client
    config.vm.define :client do |client|
        client.vm.network :private_network, ip: "192.168.10.90"
        client.vm.host_name = "client"
        client.vm.provider :virtualbox do |vb|
            vb.memory = 1024
            vb.cpus = 2
        end
    end

    # Make the glusterfs cluster, each with DISKS number of drives
    (0..NODES-1).each do |i|
        config.vm.define "storage#{i}" do |storage|
            storage.vm.hostname = "storage#{i}"
            storage.vm.network :private_network, ip: "192.168.10.10#{i}"
            (0..DISKS-1).each do |d|
                storage.vm.provider :virtualbox do |vb|
                    vb.customize [ "createhd", "--filename", "disk-#{i}-#{d}.vdi", "--size", 500*1024 ]
                    vb.customize [ "storageattach", :id, "--storagectl", "SATA Controller", "--port", 3+d, "--device", 0, "--type", "hdd", "--medium", "disk-#{i}-#{d}.vdi" ]
                    vb.memory = 1024
                    vb.cpus = 2
                end
            end

            if i == (NODES-1)
                # View the documentation for the provider you're using for more
                # information on available options.
                storage.vm.provision :ansible do |ansible|
                    ansible.limit = "all"
                    ansible.playbook = "site.yml"
                    ansible.groups = {
                        "client" => ["client"],
                        "heketi" => ["storage0"],
                        "gluster" => (0..NODES-1).map {|j| "storage#{j}"},
                    }
                end
            end
        end

    end
end

