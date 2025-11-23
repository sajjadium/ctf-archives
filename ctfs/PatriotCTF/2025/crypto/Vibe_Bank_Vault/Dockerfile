FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y socat
# Copy the challenge file
COPY vibe_vault.py .

# Create a non-root user
RUN useradd -m ctf
USER ctf

# Expose the challenge port
EXPOSE 6666

# Run the challenge
CMD ["socat", "TCP-LISTEN:6666,reuseaddr,fork", "EXEC:\"python3 vibe_vault.py\",pty,stderr,setsid,sigint,sane"]