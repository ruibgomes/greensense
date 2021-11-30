# GREENSENSE
#### Video Demo:  https://youtu.be/nTiwQothZOc
#### Description:

##### General Description

Greensense is an environmental parameter monitoring system to be implemented in household greenhouses and small greenhouses. It uses three different sensors controlled by an Arduino board. It can use several sensor sets. The system incorporates a dashboard app implemented as a web app developed in Python with the Django framework. The dashboard app is to be deployed locally on a server (I use a Raspberry Pi 3).

It uses the following hardware:
- a sunlight sensor: GROVE SUNLIGHT SENSOR (https://store.arduino.cc/grove-sunlight-sensor)
- a humidity and temperature sensor: DHT22 (https://store.arduino.cc/grove-temperature-humidity-sensor-pro)
- a soil moisture sensor: GROVE - MOISTURE SENSOR (https://store.arduino.cc/grove-moisture-sensor)
- an ARDUINO UNO WIFI REV2 board (https://store.arduino.cc/arduino-uno-wifi-rev2)

The GREENSENSE dashboard app is a web app developed in Django framework that receives the data from the Arduino board and presents the following parameters:
- Air temperature
- Air humidity
- Soil moisture
- IR light intensity
- Visible light intensity
- UV light intensity

**ATTENTION** : the app is in development mode. For deployment please follow this checklist: https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

The dashboard app also allows choosing from several implemented sets of sensors, as well to display time series of the parameters for a chosen interval of dates and performs a statistical analysis.

##### Arduino code and sensors

The dashboard app gets the values from the Arduino boards in JSON format through an API (through HTML server implemented in each Arduino board). The dashboard app gets the values for each sensor set through its unique IP address. So, each Arduino board should be configured in the local network to have a unique IP address. Each sensor set can be configured in the dashboard app ADMIN section, by manually adding the individual IP address.

The Arduino code for controlling the three sensors, the wifi module, the Arduino webserver and the JSON data formating, is in the **greensense.ino** file. In the **arduino_secrets.h** is the more sensitive network information, namely the SSID and password to connect to the local network. The Arduino code was developed in Arduino IDE (https://www.arduino.cc/en/software). Please refer to the latest stable version.

##### Django dashboard app

The dashboard web app has the function of reading and displaying the current data for a given sensor set. Also is possible to choose a date interval and perform a statistical analysis of that period, and show plots of those values. It is also possible to print a report for that analysis. In the **Admin** section is possible to add more set of sensors, and consult all values in the database.

In the **django_files** folders are the Django framework files. Django is a Model View Template (MVT) framework. Templates give the structure of the app (presentation layer); Model handles the database. View controls all logic of the app. A better understanding of MVT structure can be found here: https://www.javatpoint.com/django-mvt. 

The MVT coding is done in the following files:

- **django_files/dash/views.py** . Here you can find the main function to fetch data from the sensors, the selection of a date interval, and the statistical analysis.
- **django_files/dash/models.py** . Here are the database structure, coded in python (Django converts to SQL). Tables are for the sensor sets and the sensor values over time.
- The folder **django_files/templates** contains the HTML codes and **django_files/static** the images and CSS files.

The data acquisition and database storage are done by Celery, a simple, flexible, and reliable distributed system (Python library) to process vast amounts of messages while providing operations with the tools required to maintain such a system.

More information on the use of Celery can be found at: https://docs.celeryproject.org/en/stable/django/index.html

Celery works with a message broker. In this project, RabbitMQ was used. More info on how to install and configure: https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#rabbitmq

There is also the need for setting periodic tasks to acquire the data. This is done by Celery-beat (https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html).

Configurations for Celery are in the **django_files/greensense/celery.py** file. The executed taks are coded in **django_files/dash/tasks.py** file.

To start Celery worker, Celery beat and RabbitMQ broker, please read the following links:

- https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#starting-the-worker-process
- https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html#starting-the-scheduler
- https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/rabbitmq.html#broker-rabbitmq

The system is set to use **PostgreSQL**. This can be changed in **django_files/greensense/settings.py**. Since Django creates and handles all database structures (in the **django_files/dash/models.py** file), no special SQL coding was needed.

Auxiliary functions (plot functions) are in **django_files/dash/utils.py** file.

Since setting up a Django project is a little bit complex, I recomend to follow the official Django documentation: https://docs.djangoproject.com/en/3.2/.

The Django web app code was developed with Visual Studio Code. (https://code.visualstudio.com) 
