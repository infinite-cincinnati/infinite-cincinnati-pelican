include common.mk

MODULES=tests

CB := $(shell git branch --show-current)

all:
	@echo "no default make rule defined"

help:
	cat Makefile

rosters:
	scripts/make_roster_pages.py

requirements:
	python3 -m pip install --upgrade -r requirements.txt

test:
	pytest -sv

release_main:
	@echo "Releasing current branch $(CB) to main"
	scripts/release.sh $(CB) main

deploy_local:
	scripts/deploy_local.sh

deploy:
	scripts/deploy_ghpages.sh
