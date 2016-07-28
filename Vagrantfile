# -*- mode: ruby -*-
# vi: set ft=ruby :


$TRUSTY = <<SCRIPT

# Herokuish
sudo docker pull gliderlabs/herokuish
sudo mkdir -p /odooku/cache /odooku/build /odooku/filestore
sudo chown -R $USER /odooku

# Postgresql
sudo docker run \
  --name postgres \
  -e POSTGRES_PASSWORD=odoo \
  -e POSTGRES_USER=odoo \
  -d \
  --net host \
  postgres:9.5

sleep 10
DATABASE=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1`
sudo docker exec postgres createdb -U odoo $DATABASE
export DATABASE_URL=postgres://odoo:odoo@localhost:5432/$DATABASE

sudo tee /etc/environment > /dev/null <<EOF
export DATABASE_URL=$DATABASE_URL
export PORT=8000
EOF

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
