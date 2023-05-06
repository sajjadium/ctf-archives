FROM ruby:3.0.1-alpine3.13

# Create app directory
RUN mkdir -p /app
WORKDIR /app

# Bundle app source
COPY index.rb flag /app/

# Install dependencies
RUN apk add socat

# Set non root user
RUN adduser -D user -h /home/user -s /bin/bash user
RUN chown -R user:user /home/user
RUN chmod -R 755 .

USER user
ENV HOME /home/user

EXPOSE 3000
CMD ["socat", "-dd", "-T60", "TCP4-LISTEN:3000,fork,reuseaddr", "EXEC:ruby /app/index.rb,pty,setuid=user,echo=0,raw,iexten=0"]