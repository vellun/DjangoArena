# DjangoArena

[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-5/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-5/-/commits/main)

Django Arena is a competition platform where users(in particular djangists) can duel and compete in writing django code.

The project contains two parts: the main application and an application for testing and scoring tasks submissions during a duel.

## Required versions

required python version - 3.9 or higher

required django version - 4.2

## Redis installation
> Django Arena uses Redis, so its installation is required

#### For Linux:

- Install redis using package manager

  ```bash
  sudo apt-get install redis-server
  ```

- Run redis-server

  ```bash
  sudo service redis-server start
  ```

#### For Windows:

- Install the zip file from gihub

  > [Download redis v7.2.4](https://github.com/redis-windows/redis-windows/releases/download/7.2.4/Redis-7.2.4-Windows-x64-cygwin.zip)

* Unzip the file
* Go to the directory and open a file named redis-server

## Project installation and running

- Install project to your pc using

  ```bash
   git clone https://gitlab.crja72.ru/django/2024/spring/course/projects/team-5.git
  ```

- Go to the project directory

  ```bash
  cd team-5
  ```

- Create virtual environment

  ```bash
  python -m venv venv
  ```

- Activate your virtual environment

  #### For Linux:

  ```bash
  source venv/bin/activate
  ```

  #### For Windows:

  ```bash
  venv/Scripts/activate
  ```

- Install dependencies you need to run app

  For production install

  ```bash
  pip install -r requirements/prod.txt
  ```

  For development install

  ```bash
  pip install -r requirements/dev.txt
  ```

  For testing install

  ```bash
  pip install -r requirements/test.txt
  ```

- Create .env file and add there data that you need
  (you can see how to configure .env in the
  test .env.template file in the root of the project)

  ```bash
  cp .env.template .env
  ```

### Running the main application

> **Important:** You must have Redis server running for the application to work

- Go to the main application directory

  ```bash
  cd django_arena
  ```

- Make and apply migrations:

  ```bash
  python manage.py makemigrations
  python migrate
  ```

- Run the main application:

  ```bash
  python manage.py runserver
  ```

### Running the application for testing

- Open a new terminal window and go to the application for testing directory

  ```bash
  cd django_arena_testing
  ```

- Activate your virtual environment

  #### For Linux:

  ```bash
  source venv/bin/activate
  ```

  #### For Windows:

  ```bash
  venv/Scripts/activate
  ```

- Apply default django migrations:

  ```bash
  python migrate
  ```

- Run the application for testing:

  ```bash
  python manage.py runserver 8001 --noreload
  ```
