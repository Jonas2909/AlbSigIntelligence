FROM alpine:latest

# Update and install dependencies
RUN apk update && \
    apk add py-pip --no-cache python3-dev arp-scan

# Upgrade pip without the --upgrade flag
RUN pip install --no-cache-dir pip --break-system-packages

# Set working directory
WORKDIR /app

# Copy requirements and scanner.py
COPY Backend/Scanner/requirements_scanner.txt /app/requirements_scanner.txt
COPY Backend/Scanner/scanner.py /app/scanner.py

# Install Python dependencies
RUN pip install -r requirements_scanner.txt --no-cache-dir --break-system-packages

# Make scanner.py executable
RUN chmod 777 scanner.py 
