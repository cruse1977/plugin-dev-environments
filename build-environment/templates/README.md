
# development environment

* docker compose pull
* docker compose build
* docker compose up

```
docker exec -it docker-develop-netbox-1 /opt/netbox/netbox/manage.py makemigrations netbox_floorplan_plugin

docker exec -it docker-develop-netbox-1 /opt/netbox/netbox/manage.py makemigrations migrate

docker exec -it docker-develop-netbox-1 /opt/netbox/netbox/manage.py createsuperuser
```