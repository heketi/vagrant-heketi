# -*- mode: ruby -*-
# vi: set ft=ruby :
#

NODES = 4
DISKS = 4

Vagrant.configure("2") do |config|
    config.vm.box = "chef/centos-7.1"
    config.vbguest.auto_update = false

    (0..NODES-1).each do |i|
        config.vm.define "storage#{i}" do |storage|
            storage.vm.hostname = "storage#{i}"
            storage.vm.network :private_network, ip: "192.168.10.10#{i}", virtualbox__intnet: true
            (0..DISKS-1).each do |d|
                storage.vm.provider :virtualbox do |vb|
                    vb.customize [ "createhd", "--filename", "disk-#{i}-#{d}.vdi", "--size", 500*1024 ]
                    vb.customize [ "storageattach", :id, "--storagectl", "SATA Controller", "--port", 3+d, "--device", 0, "--type", "hdd", "--medium", "disk-#{i}-#{d}.vdi" ]
                    vb.memory = 1024
                    vb.cpus = 2
                end
            end
        end
    end

    # View the documentation for the provider you're using for more
    # information on available options.
    config.vm.provision :ansible do |ansible|
        ansible.limit = "all"
        ansible.playbook = "site.yml"
    end
end


#- name: install glusterfs
#  yum: name={{ item }} state=present
#  with_items:
#    - glusterfs-cli
#    - glusterfs-libs
#    - glusterfs
#    - glusterfs-fuse
#    - glusterfs-api

