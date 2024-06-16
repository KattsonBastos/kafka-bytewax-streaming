#!/bin/bash

### -- this script copies ./pinot-*.json to the pinot-controller container and then creates table and schema

echo "Copying files.."
TABLE_PATH=/tmp/pinot-table.json
SCHEMA_PATH=/tmp/pinot-schema.json

docker cp pinot-table.json pinot-controller:$TABLE_PATH
docker cp pinot-schema.json pinot-controller:$SCHEMA_PATH

echo "Creating schema.."
docker exec -it pinot-controller /opt/pinot/bin/pinot-admin.sh AddSchema \
  -schemaFile $SCHEMA_PATH \
  -controllerHost pinot-controller \
  -controllerPort 9000 -exec

echo "Creating table.."
docker exec -it pinot-controller /opt/pinot/bin/pinot-admin.sh AddTable \
  -schemaFile $SCHEMA_PATH \
  -tableConfigFile $TABLE_PATH \
  -controllerHost pinot-controller \
  -controllerPort 9000 -exec
