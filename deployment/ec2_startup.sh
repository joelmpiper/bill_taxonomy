#!/bin/bash
sudo apt-get update
sudo apt-get install -y git apt-transport-https ca-certificates curl software-properties-common awscli
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-compose
sudo usermod -aG docker ${USER}

mkdir /home/ubuntu/repos
# Clone your project
git clone https://github.com/joelmpiper/bill_taxonomy.git /home/ubuntu/repos/bill_taxonomy
cd /home/ubuntu/repos/bill_taxonomy/deployment

# Set environment variables
export LOCAL=false

# Run Docker Compose
docker-compose up -d