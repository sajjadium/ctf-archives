#!/bin/bash

set -eo pipefail

#
# Move resources out of the temp directory and change their ownership
#
mv /tmp/entrypoint.sh /entrypoint.sh
chmod +x /entrypoint.sh

#
# Initialize the data directories
#
mkdir -p $ARCHIVA_BASE
mkdir -p $TEMPLATE_ROOT

#
# Initialize the template directories
#
IFS=',' read -r -a array <<< "$EXTERNAL_DATA_DIRS"
for datadir in "${array[@]}"
do
  if [ -e ${ARCHIVA_HOME}/${datadir} ]
  then
    mv -v ${ARCHIVA_HOME}/${datadir} ${TEMPLATE_ROOT}/${datadir}
  fi
done

#
# The template config directory template should only include the
# archiva.xml and shared.xml files.
#
mv ${TEMPLATE_ROOT}/conf ${TEMPLATE_ROOT}/conf-orig
mkdir ${TEMPLATE_ROOT}/conf
mv /tmp/archiva.xml ${TEMPLATE_ROOT}/conf
cp ${TEMPLATE_ROOT}/conf-orig/shared.xml ${TEMPLATE_ROOT}/conf

# Ensure correct ownership of all of the files that we'll manage.
chown -R archiva:archiva $ARCHIVA_BASE $TEMPLATE_ROOT
