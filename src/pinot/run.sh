#!/bin/bash


echo "Copying files.."
TABLE_PATH=/tmp/pinot-table.json
SCHEMA_PATH=/tmp/pinot-schema.json

docker cp pinot-table.json pinot-controller:/tmp/pinot-table.json
docker cp pinot-schema.json pinot-controller:/tmp/pinot-schema.json
docker cp pinot-tenant.json pinot-controller:/tmp/pinot-tenant.json

echo "Creating schema.."
# docker exec -it pinot-controller /opt/pinot/bin/pinot-admin.sh AddSchema \
#   -schemaFile /tmp/pinot-schema.json \
#   -controllerHost pinot-controller \
#   -controllerPort 9000 -exec

echo "Creating table.."
docker exec -it pinot-controller /opt/pinot/bin/pinot-admin.sh AddTable \
  -schemaFile /tmp/pinot-schema.json \
  -tableConfigFile /tmp/pinot-table.json \
  -controllerHost pinot-controller \
  -controllerPort 9000 -exec

# docker exec -it pinot-controller /opt/pinot/bin/pinot-admin.sh AddTable \
# -tableConfigFile /tmp/pinot-table.json -exec



# /opt/pinot/bin/pinot-admin.sh AddSchema   -schemaFile pinot-schema.json -exec