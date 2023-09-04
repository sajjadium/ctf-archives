FROM drupal:10.1.2-php8.1-apache-bookworm

RUN composer require drush/drush && composer install
RUN drush site:install --site-name=default --db-url=sqlite://sites/default/files/.ht.sqlite -y
COPY ./modules /opt/drupal/web/modules
COPY db.sqlite /opt/drupal/web/sites/default/files/.ht.sqlite

RUN chown -R www-data:www-data /opt/drupal/web/sites/default/files/