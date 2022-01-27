#!/bin/bash

docker-compose exec backend-dcf python manage.py update_heavycomputation_instances_status "$@"
