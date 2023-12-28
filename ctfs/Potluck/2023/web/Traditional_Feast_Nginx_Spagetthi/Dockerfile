# Use the nginx alpine image as the base
FROM nginx:1.25.3-alpine


ARG FLAG=potluck{placeholder}

# Copy the nginx configuration file
COPY conf/nginx.conf /etc/nginx/nginx.conf
RUN echo "set \$flag \"${FLAG}\";" > /etc/nginx/flag.conf

# Copy the xsl, njs, and www directories
COPY xsl/ /etc/nginx/xsl/
COPY njs/ /etc/nginx/njs/
COPY www/ /var/www/

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]