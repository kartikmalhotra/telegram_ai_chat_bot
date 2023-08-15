# Create virtual environment (optional)

python3 -m venv venv
source venv/bin/activate

# Run the following command to start your first app

python manage.py startapp testdb

## Install all requirements:

pip install -r requirements.txt

### Create superuser to get access to admin panel

python manage.py createsuperuser

#### Create a project and start a new application

django-admin startproject myproject
cd myproject
django-admin startapp userapp

### List of command that chat bot support

help - Learn how to interact with me
balance - Check how many credits you have
buy - Buy more credits to interact with me
restart - Restart the conversation
threestory - Receive three stories per day
twostory - Receive two stories per day
onestory - Receive one story per day
nostory - Disable story updatess
