# -*- mode: ruby -*-
# vi: set ft=ruby :


$TRUSTY = <<SCRIPT

sudo curl -sSL https://get.docker.com/ | sh
sudo usermod -aG docker ${USER}

sudo mkdir /buildstep
sudo chown ${USER} /buildstep
git clone https://github.com/progrium/buildstep /buildstep
cd /buildstep && make build

# Postgresql
sudo docker run \
  --name postgres \
  -e POSTGRES_PASSWORD=odoo \
  -e POSTGRES_USER=odoo \
  -d \
  --net host \
  postgres:latest

DATABASE=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1`
sudo docker exec postgres createdb -U odoo $DATABASE
export DATABASE_URL=postgres://odoo:odoo@localhost:6212/$DATABASE

SCRIPT


# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder '.', '/vagrant'
  config.vm.provision "shell", inline: $TRUSTY, privileged: false

  config.vm.network "forwarded_port", guest: 80, host: 8000
  config.vm.network "forwarded_port", guest: 443, host: 8443
  config.vm.provider "virtualbox" do |vb|
     vb.memory = 1024
     vb.cpus = 1
  end

end
