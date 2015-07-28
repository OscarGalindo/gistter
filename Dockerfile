######################################
# Dockerfile to deploy Gistter 
#
# Build command:
#  $ docker build -t gistter .
#  $ docker run -p 5000:80 gistter
#
#####################################

# Set the base image to Ubuntu
FROM ubuntu:14.04

# Me :-D
MAINTAINER kaseOga <galindero@gmail.com>

# Add the application resources URL and update the source list
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list
RUN apt-get -y update

# Essentials
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

# Python
RUN apt-get install -y python python-dev python-distribute python-pip

# Clone the project into ~/gistter
WORKDIR ~/gistter
RUN git clone https://github.com/kaseOga/gistter .

# Install requirements
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Launch server
CMD python manage.py runserver
