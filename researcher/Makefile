
all: build


build: 
	./build.sh


deploy: build
	./deploy.sh

run: 
	./run.sh topics.txt

run_docker: build
	./run_docker.sh


.PHONY: all build deploy run run_docker