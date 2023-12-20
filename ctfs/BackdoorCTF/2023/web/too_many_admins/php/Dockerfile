FROM php:8.0-apache

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=PASSWORD
ENV MYSQL_DATABASE=DATABASE
ENV MYSQL_USER=root

# Install the mysqli extension
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

# Update and upgrade the system packages
RUN apt-get update && apt-get upgrade -y

# Your additional instructions go here
