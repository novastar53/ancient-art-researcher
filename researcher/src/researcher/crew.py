import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from researcher.tools.image_downloader import ImagesDownloader
from researcher.tools.content_uploader import ContentUploader
from researcher.tools.description_generator import DescriptionGenerator
from researcher.tools.content_checker import ContentUploadChecker

from crewai_tools import (
    SerperDevTool,
)

load_dotenv()


# Initialize tools
image_search_tool = SerperDevTool(
    search_url="https://google.serper.dev/images",
)
image_downloader_tool = ImagesDownloader()
content_uploader_tool = ContentUploader()
content_checker_tool = ContentUploadChecker()
description_generator_tool = DescriptionGenerator()


tools = [image_search_tool, 
		 image_downloader_tool, 
		 content_uploader_tool, 
		 content_checker_tool,
		 description_generator_tool]

@CrewBase
class ResearcherCrew():
	"""Researcher crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=tools,
			verbose=True
		)
	
	@task
	def search_for_images(self) -> Task:
		return Task(
			config=self.tasks_config['search_for_images'],
			tools=tools,
			agent=self.researcher(),
		)
	

	@task
	def download_images(self) -> Task:
		return Task(
			config=self.tasks_config['download_and_generate_descriptions'],
			tools=tools,
			agent=self.researcher()

		)	
	

	@task
	def upload_content(self) -> Task:
		return Task(
			config=self.tasks_config['upload_content'],
			tools=tools,
			agent=self.researcher()
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Ancient Art Research crew"""
		return Crew(
			manager_llm=ChatOpenAI(model_name="gpt-4o", temperature=0),
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			planning=True,
			memory=True,
			verbose=2,

			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)