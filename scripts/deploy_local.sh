#!/bin/bash

set -euo pipefail

if [ -z ${INFINITE_PELICAN_HOME+x} ]; then
	echo 'You must set the $INFINITE_PELICAN_HOME environment variable to proceed.'
    echo 'Try sourcing environment.{STAGE}'
	exit 1
else 
	echo "\$INFINITE_PELICAN_HOME is set to '$INFINITE_PELICAN_HOME'"
fi

(
cd ${INFINITE_PELICAN_HOME}/pelican
rm -fr output
echo "Generating pelican content..."
pelican content
(
cd output
python -m http.server 8888
)
)
