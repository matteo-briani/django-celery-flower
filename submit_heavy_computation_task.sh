#!/bin/bash

docker-compose exec backend-dcf python manage.py submit_heavy_computation_task "$@"
