# Use an official PHP runtime as the base image
FROM php:7.4-apache

# Install mysqli extension
RUN docker-php-ext-install mysqli

# Configure Apache to serve PHP files
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# Set the ServerName directive
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

RUN a2enmod rewrite

# Copy the flag.txt file from the build context into the container
COPY flag.txt /

# Set the working directory to /var/www/html
WORKDIR /var/www/html

# Copy the PHP application files from the src directory into the container
COPY . /var/www/html/

# Expose port 80 for Apache
EXPOSE 80

# Start Apache when the container runs
CMD ["apache2-foreground"]
