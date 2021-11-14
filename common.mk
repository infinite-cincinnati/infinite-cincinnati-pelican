SHELL=/bin/bash

ifeq ($(shell echo ${INFINITE_PELICAN_HOME}),)
$(error Environment variable INFINITE_PELICAN_HOME not defined. Please run "source environment" in the golly-pelican repo root directory before running make commands)
endif

#ifeq ($(shell which jq),)
#$(error Please install jq using "apt-get install jq" or "brew install jq")
#endif

