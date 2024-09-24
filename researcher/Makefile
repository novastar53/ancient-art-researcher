
all: venv init build

venv: 
	python -m venv .venv 
	. .venv/bin/activate 

init: 
	poetry lock && poetry install

build: 
	./build.sh

deploy: build
	./deploy.sh

run: 
	./run.sh topics.txt

run_docker: build
	./run_docker.sh

clean: 
	rm -rf .venv
	rm -rf dist

.PHONY: all venv init build deploy run run_docker clean