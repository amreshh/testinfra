VAGRANTFILE_API_VERSION = "2"
VAGRANTFILE_VM_BOX = "centos/7"

$provision = <<SCRIPT
date
SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # server1
  config.vm.define "server1" do |server1|
    server1.ssh.insert_key = false
    server1.vm.box = VAGRANTFILE_VM_BOX
    server1.vm.hostname = "server1"
    server1.vm.network "private_network", ip: "192.168.110.21"
    server1.vm.provider :virtualbox do |vb|
      vb.gui  = true
      vb.name = "server1"
      vb.customize ["modifyvm", :id, "--memory", "1024", "--cpus", "1"]
      vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
    end
    server1.vm.provision "shell", inline: $provision
  end

  # server2
  config.vm.define "server2" do |server2|
    server2.ssh.insert_key = false
    server2.vm.box = VAGRANTFILE_VM_BOX
    server2.vm.hostname = "server2"
    server2.vm.network "private_network", ip: "192.168.110.31"
    server2.vm.provider :virtualbox do |vb|
      vb.gui  = true
      vb.name = "server2"
      vb.customize ["modifyvm", :id, "--memory", "1024", "--cpus", "1"]
      vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
    end
    server2.vm.provision "shell", inline: $provision
  end
end
