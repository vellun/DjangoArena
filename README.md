# DjangoArena

Django Arena is a project that allows djangists to compete in writing industrial code in django.

[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-5/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-5/-/commits/main)

[![coverage report](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-5/badges/main/coverage.svg)](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-5/-/commits/main)

# Installation
## For Windows:
* Create a virtual environment using the command:
```bash
python -m venv (name)
```

* Activate the virtual environment:
```bash
venv/Scripts/activate
```

* Install all necessary dependencies:

to install all:
```bash
pip install -r requirements/test.txt
```
to install dev and prod requirements:
```bash
pip install -r requirements/dev.txt
```
to install prod requirements:
```bash
pip install -r requirements/prod.txt
```

* Go to the project file:
```bash
cd django_arena
```

* Make and use migrations using the following commands:
```bash
python manage.py makemigrations
python migrate
```

* Check the performance of the project with the help of tests:
```bash
python manage.py test
```

* After passing the tests, we launch the server:
```bash
python manage.py runserver
```


## For Linux:
* Create a virtual environment using the command:
```bash
python -m venv (name_venv)
```

* Activate the virtual environment:
```bash
source venv/bin/activate
```

* Install all necessary dependencies:

to install all:
```bash
pip install -r requirements/test.txt
```
to install dev and prod requirements:
```bash
pip install -r requirements/dev.txt
```
to install prod requirements:
```bash
pip install -r requirements/prod.txt
```

* Go to the project file:
```bash
cd django_arena
```

* Make and use migrations using the following commands:
```bash
python manage.py makemigrations
python migrate
```

* Check the performance of the project with the help of tests:
```bash
python manage.py test
```

* After passing the tests, we launch the server:
```bash
python manage.py runserver
```