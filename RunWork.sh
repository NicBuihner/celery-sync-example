#!/bin/bash

# Setup because we run on GCP
export TZ=America/Los_Angeles
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
locale-gen en_US.UTF-8
update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

# Backend for Celery
apt update
DEBIAN_FRONTEND=noninteractive apt install -y rabbitmq-server

# Somewhere in here you git clone your code containing the requirements.txt
# into this directory.

# Install the Python requirements
pip3 install -U -r requirements.txt

# Bash is already ugly, I saw this echo ""; trick somewhere and thinks it
# makes things easier to read.

# Start and background the Celery worker
echo ""; \
    GOOGLE_APPLICATION_CREDENTIALS="/path/to/service.json" \
    GOOGLE_USER="someuser@somedomain.com" \
    celery -A GoogleTasks worker &
sleep 3

# Run the sync
echo ""; \
    python3 ./GoogleSync.py

# Wait until the Celery queue is empty
until rabbitmqctl list_queues | grep -qP '^celery\s+0$'
do
    sleep 1
done

# Terminate the GCP instance
name=$(hostname)
zone=$(curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/zone | cut -d'/' -f4)
gcloud compute instances delete $name --zone=$zone --quiet
