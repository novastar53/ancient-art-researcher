
all: venv init build deploy

venv: 
	python -m venv .venv 
	. .venv/bin/activate

init: 
	poetry lock && poetry install	

build:
	./build.sh

deploy:
	./deploy.sh