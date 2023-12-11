# Generación de Energía Monitoring API

Esta es la API para la aplicación de generación de energía. Permite gestionar dispositivos, lecturas y mantenimientos asociados a la generación de energía.

## Requisitos

- Python 3.x
- MariaDB (puede usar XAMPP para una configuración sencilla)

## Configuración del entorno virtual

1. **Clonar el Repositorio:**

   ```bash
   git clone https://github.com/StevenSanchezEs/generacion_energia_monitoring.git

2.**Acceder al Directorio del Proyecto:**

> cd generacion-energia-monitoring

3.**Crear y Activar el Entorno Virtual:**

> python -m venv env
source venv/bin/activate      # En sistemas basados en Unix 

> python -m venv env
> .\venv\Scripts\activate       # En sistemas basados en Windows (PowerShell)

4.**Instalar Dependencias:**

> pip install -r requirements.txt

## Configuración de la Base de Datos
1.**Descargar XAMPP**
[-->XAMPP<--](https://www.apachefriends.org/index.html)

2.**Instalar XAMPP**

3.**Iniciar el Servidor de MariaDB desde XAMPP**

4.**Acceder a la Consola de MariaDB**

> mysql -u root

5.**Crear una Base de Datos**

> CREATE DATABASE monitoring;

6.**Configurar credenciales en generacion_energia_monitoring/settings.py para la conexión con la BDD**

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'monitoring',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
    }
7.**Crear Migraciones y Migrar**

> python manage.py makemigrations
python manage.py migrate

## Ejecución del Proyecto

1.**Iniciar el Servidor de Desarrollo**

> python manage.py runserver

2.**Acceder a las API'S para Explorar y Probar**
[-->Swagger<--](http://127.0.0.1:8000/api/swagger/)
[-->Redoc<--](http://127.0.0.1:8000/api/redoc/)

**Diagrama entidad-relación**
[-->Descargar diagrama<--](https://1drv.ms/i/s!ArXfZ0krp14qoie0UKHmZdajbxcX?e=g4dGAq)

¡Listo para comenzar con tu proyecto de generación de energía! ✨🚀