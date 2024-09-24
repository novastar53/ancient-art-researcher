
all: venv init build deploy

venv: 
	python -m venv .venv 
	. .venv/bin/activate

init: 
	. .venv/bin/activate && poetry lock && poetry install	

build:
	. .venv/bin/activate && ./build.sh

deploy:
	. .venv/bin/activate && ./deploy.sh