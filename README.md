# Pasos a realizar

### Crear el entorno virtual
- virtualenv env
- source env/Scripts/activate

### Instalaciones
- pip install django
- pip install mysqlclient
- pip install gunicorn
- pip freeze > requirements.txt
### Crear proyecto y app
- django-admin startproject djangocrud .
- django-admin startapp tasks

### Modificaciones:
INSTALLED_APPS = [
...
    # Aplicaciones instaladas
    'tasks',
]
- CSRF_TRUSTED_ORIGINS = ['https://template-django-production-6e65.up.railway.app']

### crear las tablas en la db
- django-admin startapp tasks
- python manage.py makemigrations
### correr el proyecto
- python manage.py runserver

## Notas:
### En el html:
- {{form.as_p}}: lo coloca cada uno en una linea 
- <form action="/signup/", method="POST">: al hacer click en el boton, envia los datos a "/signup/". Si no coloco "action", me reenvia a la misma vista automaticamente
- {% csrf_token %}: Para enviar los datos por POST de manera segura 
- user.is_authenticated: revisa si existe una cookie (sesion) de un usuario
#### en base:
    - {% block content %}
    - {% endblock %}
#### en el resto:
    - {% extends "base.html" %}
### en el view
- request.POST:   obtiene un diccionario con los datos con clave el name en html