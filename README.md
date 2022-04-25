# Movies-Site

## Stack Details

Python = 3.2

Django = 4.0

## Setup Project

### Run Project

**Install Requirements**

`pip install -r requirements.txt`

**Store the following environment variables**

```angular2html
STRIPE_SECRET_KEY
STRIPE_PUBLIC_KEY
STRIPE_WEBHOOK_SECRET
EMAIL_HOST
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
API_KEY
```
**Make Migrations**

`python manage.py makemigrations`

**Apply Migrations**

`python manage.py migrate`

**Run Server**

`python manage.py runserver`

**Create Super User**

`python manage.py createsuperuser`

### Run Script

Run the following script to scrap movies and save inside the database

`python manage.py runscript import_movies;`

