from waitress import serve
from django_project.wsgi import application

if __name__ == '__main__':
    serve(application, port='8080')