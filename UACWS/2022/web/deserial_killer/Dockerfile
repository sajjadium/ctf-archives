FROM php:7.4-apache

COPY . /var/www/html/

RUN apt update && apt install -y sqlite3
RUN apt clean

# Create sqlite database
RUN sqlite3 -line app.db "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL, pic_path VARCHAR(255))";
RUN sqlite3 -line app.db "INSERT INTO users(username, password, pic_path) VALUES ('admin', 'admin', '/var/www/html/avatar/avatar.jpg')";

# Change Port
RUN sed -i "1s/.*/<VirtualHost *:8000>/" /etc/apache2/sites-available/000-default.conf
RUN echo "Listen 8000" > /etc/apache2/ports.conf

RUN chown -R www-data:www-data /var/www/html/ && mv /var/www/html/flag /

EXPOSE 8000
