import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from researcher.tools.image_downloader import ImagesDownloader
from researcher.tools.image_uploader import ImageUploader
from researcher.tools.content_uploader import ContentUploader

from crewai_tools import (
    SerperDevTool,
	FirecrawlScrapeWebsiteTool
)


# Initialize tools
image_search_tool = SerperDevTool(
    search_url="https://google.serper.dev/images",
    n_results=3,
)
website_scrape_tool = FirecrawlScrapeWebsiteTool(api_key=os.environ['FIRECRAWL_API_KEY'])
image_downloader_tool = ImagesDownloader()
image_uploader_tool = ImageUploader()
content_uploader_tool = ContentUploader()

@CrewBase
class ResearcherCrew():
	"""Researcher crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def image_finder(self) -> Agent:
		return Agent(
			config=self.agents_config['image_finder'],
			tools=[image_search_tool, image_downloader_tool, image_uploader_tool, content_uploader_tool, website_scrape_tool],
			verbose=True
		)
	
	@task
	def image_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['image_research_task'],
			agent=self.image_finder(),
			tools=[image_downloader_tool, image_search_tool, image_uploader_tool, content_uploader_tool, website_scrape_tool],
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the Ancient Art Research crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)