# Game Crud

This project consists of restful APIs responsible for CRUD to store the game data and its author.

## Technical Stack

Since **FastAPI** is modern day framework which provides asynchronous processing of requests which makes it fast in comparision of django and flask as well as it also enables to use asynchronous orms to interact with DB. Two such ORMs in python are SQLAlchemy and Tortoise-ORM. Since Tortoise-ORM is very simple so for small projects it is useful to use it. Hence I have used FastAPI framework along with **Tortoise-ORM** for the project.

## Schema (game/models.py)

Schema to use here was very simple. I was supposed to use four fields in the game table, url, name, published_data and author. I could have made author a text field but I tried a more subtle version and created a table for authors too. Since a game can have many authors and one author can publish many games so made the relationship many to many.

This schema can be extended to solve other problems like making authors a user or to provide the APIs for all the games published by some author and games can be grouped accordingly.

## Project Setup and Commands

This project has been developed with python 3.8. To use this project, clone the repo and go to the project directory and run (Before running consider creating virtual environment by useing `python -m venv env`  and for activating use `env/Scripts/activate`):

`pip install -r requirements.txt`

Set up the database. This project uses postgreSQL but other relational databases can also be used. Configure the database in the config.py file and change env there to local. Then to create tables in databases run:

`python manage.py migrate first time`

For later changes and migrations use:

`python manage.py migrate`

Now before running server, you can configure the port and host in config.py file. By default this will run server at 10000 port and localhost. To run server use:

`python manage.py runserver`

Now go to [localhost:10000/docs]([localhost:10000/docs]()) to get open API specifications.

## Other Information about the project

This project contains only six APIs which clearly are not sufficient to handle both authers and games. For that more APIs can easily be developed.
