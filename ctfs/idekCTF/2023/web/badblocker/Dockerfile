FROM python:latest

# Copy files
RUN mkdir /app
WORKDIR /app
COPY challenge .

# Install dependencies
RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

# Set port
ENV PORT 1337

# Set user
USER nobody

# Run app
CMD python3 app.py