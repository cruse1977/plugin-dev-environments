# plugin-dev-environments

## Purpose

 Script to generate docker environments to provide editable (or not) plugin development environments 

 * selectable netbox version
 * optional netbox-branching installation 
 * git or pip install of selected plugin
 
# Usage

```
cd build-environment/
./run-builder.sh
```

 Then follow inbuilt instructions.

# Tip:

if you ever need to remove all docker images/volumes (warning, danger, etc) 

```
#!/bin/bash

docker system prune -f
docker volume list | awk '{print $2}' | xargs docker volume rm 
```
