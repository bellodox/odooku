# -*- mode: ruby -*-
# vi: set ft=ruby :


$TRUSTY = <<SCRIPT

# Prepare vagrant directories
mkdir -p /vagrant/data/s3

# Herokuish
sudo docker pull gliderlabs/herokuish
sudo mkdir -p /odooku /odooku/cache
sudo chown -R $USER /odooku
touch /odooku/env.mk

# Postgresql
sudo docker run \
  --name postgres \
  --restart always \
  -e POSTGRES_PASSWORD=odoo \
  -e POSTGRES_USER=odoo \
  -d \
  --net host \
  postgres:9.5

# Redis
sudo docker run \
  --name redis \
  --restart always \
  -d \
  --net host \
  redis

# S3
sudo docker run \
  --name s3 \
  --restart always \
  -d \
  -v /vagrant/data/s3:/fakes3_root \
  --net host \
  lphoward/fake-s3

sleep 10
cd /vagrant && sudo make new-env

SCRIPT


# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  config.vm.box = "box-cutter/ubuntu1404-docker"
  config.vm.synced_folder '.', '/vagrant'
  config.vm.provision "shell", inline: $TRUSTY, privileged: false

  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8443, host: 8443
  config.vm.provider "virtualbox" do |vb|
     vb.memory = 2048
     vb.cpus = 2
  end

end
