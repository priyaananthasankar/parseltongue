# Install Docker through this arduous process to make sure the latest docker is installed from the 
# Docker site and not Ubuntu's site

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-cache policy docker-ce
sudo apt-get install -y docker-ce

# Goto your project directory
cd CampingGearProject

# Install Azure CLI
AZ_REPO=$(lsb_release -cs)
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" | \
    sudo tee /etc/apt/sources.list.d/azure-cli.list
curl -L https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo apt-get install apt-transport-https azure-cli


#Install python3.6 laboriously

wget -q https://packages.microsoft.com/config/ubuntu/16.04/packages-microsoft-prod.deb
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y azure-functions-core-tools python3.6 python3.6-venv

# Create Virtual environment

sudo python3.6 -m venv worker_env 
source ./worker_env/bin/activate
sudo python3.6 -m pip install --upgrade pip
sudo python3.6 -m pip install wheel
sudo python3.6 -m pip install setuptools

# Install dependencies
source ./worker_env/bin/activate
sudo python3.6 -m pip install -r ./requirements.txt 
sudo pip freeze

# Azure Login through service principal
az login --service-principal -u {servicePrincipal} -p {password} --tenant {tenantId}

# Deploy to Linux Consumption Plan Function App - build native deps is optional when your packages
# does not have many linux wheels on PyPI
# Also make sure your linux function app is already created. Alternately you can write scripts to always
# delete and re-create the linux function app
func azure functionapp publish campinggear101 --build-native-deps
