
all: venv init build

venv: 
	python -m venv .venv 
	. .venv/bin/activate 

init: 
	. .venv/bin/activate && poetry lock

install: 
	. .venv/bin/activate && poetry install 

build: 
	. .venv/bin/activate && ./build.sh


deploy: build
	. .venv/bin/activate && ./deploy.sh

run: 
	. .venv/bin/activate && ./run.sh topics.txt

run_docker: build
	. .venv/bin/activate && ./run_docker.sh

clean: 
	rm -rf venv
	rm -rf dist

.PHONY: all build deploy run run_docker