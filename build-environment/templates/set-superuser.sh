#!/bin/bash

docker exec -it docker-develop-netbox-1 /opt/netbox/netbox/manage.py createsuperuser

