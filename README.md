# SchoolManagementAPI
DRF School Management API. Using Postgres Database. The project will have functionality for Users, Teachers and Students.

## Create Project
```bash
mkdir SchoolManagementAPI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
django-admin startproject schoolmanagement .
django-admin startapp smapi
```
This will create our Django Project.

## Configure Project
We need to add following block into `schoolmanagement/setting.py` to add PostgresSQL project.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'demo',
        'USER': 'demo',
        'PASSWORD': 'demo',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

## Run Project
Clone the project from github.

```bash
cd SchoolManagementAPI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```
