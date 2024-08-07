# Ancient Art Research Assistant 

Welcome to the Ancient Art Research Assistant project. This project runs an agent which automates one of my major hobbies: Researching historical art on the internet and blogging about them. This agent searches the web for new images of ancient artifacts to add to its collection. It then researches any new finds and produces reports based on the info that it has collected. It allows me to review its output periodically and then direct it to create short blog posts that references one or more of the images. 

## Live Demo

A live demo of the app can be accessed [here](https://finds-viewer-uwrcgo4b7q-ue.a.run.app/).

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
poetry lock
```
```bash
poetry install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
poetry run redis
poetry run history_research_assistant
```

This starts a redis server, initializes the Ancient Art Researcher Crew, assembling the agents and assigning them tasks.
