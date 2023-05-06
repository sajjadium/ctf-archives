# Use alpine:3.17.3 as base image
FROM ubuntu:22.10

# Update cache
RUN apt-get update

# Install gcc build dependencies
RUN apt-get -y install build-essential musl netcat-traditional


# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app.
COPY ./build /app/build
COPY ./run_always.sh /app
COPY ./webroot /app/webroot
COPY ./flag.txt /app

# Build the app. We only need to do this when we make changes to it.
#RUN rm -rf build && mkdir -p build
#RUN make

# Expose port 80
EXPOSE 80

# Run the app
CMD ["./run_always.sh"]
