#!/bin/bash

docker-compose exec backend-dcf python manage.py populate_task_model
