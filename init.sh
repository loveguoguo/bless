if [ ! -d env ];
then
    echo "Creating env"
    virtualenv --no-site-packages  env
fi

echo "Installing dev package"
sudo apt-get install libmysqld-dev
sudo apt-get install python-dev

if [ -f requirement.txt ];
then
    echo "Installing requirements"
    env/bin/pip install -r requirement.txt
fi
