# Django Box - in development
*A small-scale, hobbiest-driven django application that manages makerspace inventory*

![tests](https://github.com/EDED2314/djangobox/actions/workflows/django.yml/badge.svg)

# Features 🚀
1. Inventory management: So far, this is through the admin panel, a UI will be coming shortly
2. Modular storage: In many github repos that offer templates in inventory management, they do not address the variability in the storage structure that can exist in a makerspace. What DjangoBox does is creating a tree out of every storage unit and item so that a modular design is achieved.
3. Easy set up + Any platform: With the help of python, platform support is extremely easy

## Setup👀
### Installation
So far, this project runs on python 3.10.
```bash
$ git clone https://github.com/EDED2314/djangobox.git
$ cd djangobox
(venv) $ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser # Create your initial user
$ python manage.py runserver
```

## Contributing 🏗️
1. I will check and merge changes that is beneficial to this project's goal.
2. Feel free to comment and review code!

# Future Features + Plans 🛫
I have huge hope for this project an will continue to make this the best as I can! 😎

Some features planned are:
- API Endpoints
- Docker compose files + images

