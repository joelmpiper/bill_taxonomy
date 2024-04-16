#!/bin/bash
set -xe

# Clean yum cache
sudo yum clean all

# Update system
sudo yum update -y

# Install necessary packages, resolving conflicts if necessary
sudo yum install -y git aws-cli --allowerasing
sudo yum install -y curl --exclude=curl-minimal*

# Update and install necessary packages
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Setup directory for repository and clone
mkdir -p /home/ec2-user/repos
cd /home/ec2-user/repos
git clone https://github.com/joelmpiper/bill_taxonomy.git
cd bill_taxonomy/deployment 

# Set environment variables
export LOCAL=false

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Run Docker Compose
docker-compose up -d