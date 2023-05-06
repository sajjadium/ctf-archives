#!/bin/bash

#
# See the README file for usage!
#
set -e

if [[ -z "$SMTP_HOST" && -z "$JETTY_CONFIG_PATH" ]]
then
  echo "WARNING: SMTP_HOST not set, Archiva cannot send emails!" > /dev/stderr
fi

JETTY_CONFIG_PATH=/tmp/jetty.xml
# A preventative measure to avoid OOM errors
MALLOC_ARENA_MAX=-2

#
# Initialize the volume data directories
#
IFS=',' read -r -a array <<< "$EXTERNAL_DATA_DIRS"
for datadir in "${array[@]}"
do
  if [ ! -e ${ARCHIVA_BASE}/${datadir} ]
  then
    if [ -e ${TEMPLATE_ROOT}/${datadir} ]
    then
      echo "Populating $datadir from template..."
      cp -pr ${TEMPLATE_ROOT}/${datadir} ${ARCHIVA_BASE}/${datadir}
    else
      echo "Creating empty directory for $datadir..."
      mkdir ${ARCHIVA_BASE}/${datadir}
    fi
  fi
done

#
# Setup the JVM enviroment arguments
#
export CLASSPATH=$(find /archiva/lib -name "*.jar"\
  | sed '/wrapper.jar/d' | awk '{ printf("%s:", $1) }')

JVM_OPTS=(
  "-Dappserver.home=."
  "-Dappserver.base=$ARCHIVA_BASE"
  "-Djetty.logs=${ARCHIVA_BASE}/logs"
  "-Djava.io.tmpdir=${ARCHIVA_BASE}/temp"
  "-DAsyncLoggerConfig.WaitStrategy=Block"
  "-Darchiva.repositorySessionFactory.id=jcr"
  "-XX:+UseContainerSupport"
)

#
# Set aliases to the runtime & initialization jvm
# properties used by Archiva v2
#
REDBACK_PREFIX="org.apache.archiva.redback"
REDBACK_RT_PREFIX="${REDBACK_PREFIX}RuntimeConfiguration.configurationProperties"
WEBAPP_PREFIX="org.apache.archiva.webapp"

cd ${ARCHIVA_HOME}
nohup java $JVM_EXTRA_OPTS ${JVM_OPTS[@]}\
  org.eclipse.jetty.start.Main\
  "$JETTY_CONFIG_PATH" &
exec /proxy 8081 8080