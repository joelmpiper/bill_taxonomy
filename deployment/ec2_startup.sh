#!/bin/bash
set -xe

# Clean yum cache
sudo yum clean all

# Update system
sudo yum update -y

# Install necessary packages
sudo yum install -y git aws-cli curl docker python3-virtualenv --allowerasing

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
sudo wget https://github.com/mikefarah/yq/releases/download/v4.43.1/yq_linux_amd64 -O /usr/local/bin/yq
sudo chmod +x /usr/local/bin/yq
sudo curl -L "https://github.com/docker/compose/releases/download/v2.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Use newgrp to apply the group change immediately
newgrp docker <<EONG

# Setup virtual environment for Docker Compose
mkdir -p /home/ec2-user/repos
virtualenv /home/ec2-user/docker-compose-env
source /home/ec2-user/docker-compose-env/bin/activate

# Install Docker Compose
pip install docker-compose

# Clone repository
cd /home/ec2-user/repos
git clone https://github.com/joelmpiper/bill_taxonomy.git
cd bill_taxonomy/deployment

# Run Docker Compose
./bootstrap.sh

# Deactivate virtual environment
deactivate

EONG
