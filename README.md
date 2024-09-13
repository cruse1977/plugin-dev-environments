cd build-environment/

./run-builder.sh


follow the white rabbit

if you ever need to kill everything docker
```
#!/bin/bash

docker system prune -f
docker volume list | awk '{print $2}' | xargs docker volume rm 
```
