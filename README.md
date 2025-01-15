# Installation Guide for Django Chat App

Follow these steps to set up the project on your local machine.

## 1. Clone the Repository

Clone the project repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/django-chat-app.git
cd django-chat-app
```

## 2. Create a Virtual Environment
Create and activate a virtual environment to keep dependencies isolated.

```bash

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

## 3. Install Dependencies
Install the required Python packages.

```bash
pip install django
pip install channels
pip install daphne
```


## 4. Set Up the Django Project
Create a Django project and app (if not already created).

```bash
django-admin startproject django_chatapp .
python manage.py startapp chat_app
```


## 5. Configure settings.py
Update django_chatapp/settings.py:

Add 'channels' and 'chat_app' to INSTALLED_APPS.

```bash

INSTALLED_APPS = [
    # ...
    'channels',
    'chat_app',
]
```

Set the ASGI_APPLICATION:

```bash
ASGI_APPLICATION = 'django_chatapp.asgi.application'
```

Configure the channel layers (using the InMemoryChannelLayer for development):

```bash
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
```


## 6. Create Database Migrations
Create and apply database migrations.

```bash
python manage.py makemigrations
python manage.py migrate
```



## Running the Application
Start the application using Daphne, the ASGI server compatible with Django Channels.

```bash
daphne -p 8000 django_chatapp.asgi:application
```
Note: Ensure you are in the project root directory (django-chat-app) when running this command.