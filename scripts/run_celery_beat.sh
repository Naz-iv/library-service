#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

# sh -c "rm /tmp/celerybeat-doshi.pid > /dev/null"
# Replace * with name of Django Project
sh -c "celery -A core.celery beat -l info --pidfile=/tmp/core.pid"