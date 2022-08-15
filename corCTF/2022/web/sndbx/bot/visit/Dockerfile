FROM busybox as firefox
ADD https://static.cor.team/uploads/13c932e7d65bf8eb890fc9e140cc056626c8ba6e20fbb3c41c3759778bc2e8e5/firefox.zip /
RUN unzip firefox.zip

FROM ubuntu:jammy-20220531
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install-deps firefox && rm -rf /var/lib/apt/lists/*
COPY --from=firefox /firefox ./firefox
COPY . .
CMD ["gunicorn", "-b0.0.0.0:8080", "-t60", "app:app"]
