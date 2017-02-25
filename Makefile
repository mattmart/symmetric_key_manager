init:
	pip3 install -r requirements.txt

test:
	nosetests tests --nocapture

install:
	echo "What exactly do you want me to install? Read the README"
	exit 1

