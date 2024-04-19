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

export LOCAL=false

# Run Docker Compose
docker-compose up -d

# Deactivate virtual environment
deactivate

EONG
