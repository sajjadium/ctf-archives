FROM mcr.microsoft.com/dotnet/sdk:9.0
WORKDIR /app

# Install socat
RUN apt-get update && apt-get install -y socat

# Build the app
COPY src/ ./
RUN dotnet restore
RUN dotnet publish -c Release -o out


EXPOSE 1337

# Run the app through socat
CMD ["socat", "TCP4-LISTEN:1337,reuseaddr,fork", "EXEC:dotnet /app/out/luck.dll"]