#!/bin/bash

set -eo pipefail

#
# Archiva binary parameters
#
ARCHIVA_RELEASE_VERSION=2.2.9
ARCHIVA_RELEASE_URL=${ARCHIVA_RELEASE_URL:-https://downloads.apache.org/archiva/${ARCHIVA_RELEASE_VERSION}/binaries/apache-archiva-${ARCHIVA_RELEASE_VERSION}-bin.tar.gz}
ARCHIVA_RELEASE_SHA512=$(curl "${ARCHIVA_RELEASE_URL}.sha512" | cut -f1 -d' ')

#
# Download and verify the archiva tarball. Then extract
# it to the default destination
#
echo "Downloading archiva from $ARCHIVA_RELEASE_URL"
cd /tmp/
curl -O $ARCHIVA_RELEASE_URL
ARCHIVA_RELEASE_FILENAME=$(ls -C1 | grep archiva | grep .tar.gz)
echo "ARCHIVA_RELEASE_FILENAME=${ARCHIVA_RELEASE_FILENAME}"

if [ -n "$ARCHIVA_RELEASE_SHA512" ]
then
  ACTUAL_ARCHIVA_RELEASE_SHA512="$(sha512sum /tmp/${ARCHIVA_RELEASE_FILENAME} | cut -f1 -d' ')"
  if [ "$ACTUAL_ARCHIVA_RELEASE_SHA512" != "$ARCHIVA_RELEASE_SHA512" ]
  then
    echo "archiva release sha512 (${ACTUAL_ARCHIVA_RELEASE_SHA512}) did not match expected value (${ARCHIVA_RELEASE_SHA512})"
    exit 1
  fi
else
  ACTUAL_ARCHIVA_RELEASE_MD5SUM="$(md5sum /tmp/${ARCHIVA_RELEASE_FILENAME} | cut -f1 -d' ')"
  if [ "$ACTUAL_ARCHIVA_RELEASE_MD5SUM" != "$ARCHIVA_RELEASE_MD5SUM" ]
  then
    echo "archiva release md5sum did not match expected value"
    exit 1
  fi
fi

mkdir -p $ARCHIVA_HOME && cd $ARCHIVA_HOME
tar xzf /tmp/${ARCHIVA_RELEASE_FILENAME} --strip-components 1
rm -v /tmp/${ARCHIVA_RELEASE_FILENAME}


chown -R archiva:archiva $ARCHIVA_HOME

exit 0;