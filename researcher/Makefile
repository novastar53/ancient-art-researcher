################################################################################
# Makefile
################################################################################

#-------------------------------------------------------------------------------
# Environment
#-------------------------------------------------------------------------------

VENV_ROOT := .venv
VENV := $(VENV_ROOT)/bin/activate
ENV_FILE := .env

################################################################################
# Targets
################################################################################

all: venv init build deploy

venv: 
	python -m venv $(VENV_ROOT)

init: 
	. $(VENV) && . $(ENV_FILE) && poetry lock && poetry install

build: 
	. $(VENV) && . $(ENV_FILE) && ./build.sh

deploy: build
	. $(VENV) && . $(ENV_FILE) && ./deploy.sh

run: 
	. $(VENV) && . $(ENV_FILE) && ./run.sh topics.txt

run_docker: build
	. $(VENV) && . $(ENV_FILE) && ./run_docker.sh

clean: 
	rm -rf $(VENV_ROOT)
	rm -rf dist

.PHONY: all venv init build deploy run run_docker clean