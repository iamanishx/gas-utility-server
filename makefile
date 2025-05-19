venv:
    python -m venv venv
    .\venv\Scripts\activate

install:
    pip install -r requirements.txt

migrate:
    python manage.py migrate

run:
    python manage.py runserver

create-customers:
    python xyz.py