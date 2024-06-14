#!/bin/bash

docker exec -it docker-develop-secrets-netbox-1 /opt/netbox/netbox/manage.py createsuperuser

