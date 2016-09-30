# -*- mode: ruby -*-
# vi: set ft=ruby :


$TRUSTY = <<SCRIPT

# Update and install git
sudo apt-get -y update \
  && sudo apt-get -y install git

# Herokuish
docker pull gliderlabs/herokuish

# Postgresql
docker run \
  --name postgres \
  --restart always \
  -e POSTGRES_PASSWORD=odoo \
  -e POSTGRES_USER=odoo \
  -d \
  --net host \
  postgres:9.5

# Redis
docker run \
  --name redis \
  --restart always \
  -d \
  --net host \
  redis

# S3
docker run \
  --name s3 \
  --restart always \
  -d \
  -v /odooku/s3:/fakes3_root \
  --net host \
  lphoward/fake-s3


sudo tee /etc/environment -a > /dev/null <<EOF
ODOOKU_LOCAL_PREFIX=/home/$USER/odooku
ODOOKU_SHARE_DIR=/vagrant
EOF
source /etc/environment

cd /vagrant/dev && ./manage env new && ./manage pg createdb

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
  config.vm.synced_folder '../', '/vagrant'
  config.vm.provision "shell", inline: $TRUSTY, privileged: false

  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8001, host: 8001
  config.vm.network "forwarded_port", guest: 4569, host: 4569
  config.vm.provider "virtualbox" do |provider|
     provider.memory = 4096
     provider.cpus = 2
  end

end
