#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

# Replace * with name of Django Project
sh -c "celery -A core.celery worker -l info"