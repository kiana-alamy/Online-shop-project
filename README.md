# About this Project:

Hi, This is an online shopping system project with Python & Django Framework & REST API

This project is the result of a month and a half of round-the-clock efforts
With the end of this project, I am happy that I learned new things and had good experiences
I hope to be able to complete it in the future
If you think this project might be useful for you, I will be happy if you use it and let me know if you need any changes.

How to reach me: kiana.alamy.2003@gmail.com

My address: Iran , Mashhad , Ladan street


## Technologies Used:

- Django: The web framework used for building the online shop project.
- PostgreSQL: The database management system used for storing data.
- Redis: Used for caching and as the Celery message broker.
- Celery: Used for task management, such as sending emails to customers asynchronously.
- Docker: Used for containerization and deployment of the project.
- Gunicorn: A Python WSGI HTTP server used for serving the Django application.
- Nginx: A web server used as a reverse proxy and for serving static files.
- HTML5, CSS, and JavaScript: The trio of technologies employed for front-end development, providing structure, styling, and interactivity to the web pages.
- Yasg: Swagger library used for API documentation.

# Running this project:

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

      pip install virtualenv

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

      virtualenv env

That will create a new folder env in your project directory. Next activate it with this command on mac/linux:

      source env/bin/active

Then install the project dependencies with

      pip install -r requirements.txt

Now you can run the project with this command

      python manage.py runserver

Note if you want payments or email or sms to work you will need to enter your own Stripe API keys into the .env file in the settings files.

# Features:

- The appropriate template is used
- A functional profile is created for each user
- You can change the address during the purchase confirmation
- A comment section is added for each product
