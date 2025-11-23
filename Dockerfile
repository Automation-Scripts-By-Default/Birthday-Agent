# Use an official Python runtime as a base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for MariaDB connector
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    cron \
    gcc \
    nano \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the crontab file into the container
COPY cron_job /etc/cron.d/birthday-agent-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/birthday-agent-cron

# Apply cron job
RUN crontab /etc/cron.d/birthday-agent-cron

# Create log file for cron output
RUN touch /var/log/birthday-agent.log

# Run cron in the foreground
CMD ["cron", "-f"]