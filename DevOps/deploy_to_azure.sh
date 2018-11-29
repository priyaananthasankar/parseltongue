# install az 
AZ_REPO=$(lsb_release -cs)
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" | \
    sudo tee /etc/apt/sources.list.d/azure-cli.list
curl -L https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo apt-get install apt-transport-https azure-cli
# login
az login --service-principal -u  http://PythonFunctionServicePrincipal -p test --tenant 72f988bf-86f1-41af-91ab-2d7cd011db47
# install extension
az extension add --source https://functionscdn.azureedge.net/public/docs/functionapp-0.0.2-py2.py3-none-any.whl --yes && 
az extension list
# install requirements
wget -q https://packages.microsoft.com/config/ubuntu/16.04/packages-microsoft-prod.deb
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y azure-functions-core-tools python3.6 python3.6-venv
sudo python3.6 -m venv env 
source ./env/bin/activate
sudo python3.6 -m pip install --upgrade pip
sudo python3.6 -m pip install wheel
sudo python3.6 -m pip install setuptools
sudo python3.6 -m pip install -r  _ImageClassifier-CI/dist/requirements.txt
# create function
source env/bin/activate
func init _ImageClassifier-CI/dist --worker-runtime python
# publish function 
az functionapp createpreviewapp -n imageclassifier35 -g  pythonapptest -l "WestUS" -s pythonappstorage --runtime python --is-linux && 
func azure functionapp publish imageclassifier35 --force --build-native-deps --debug
