from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
from history_research_assistant.tools.image_downloader import ImagesDownloader
from history_research_assistant.tools.google_drive_uploader import GoogleDriveUploader

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool


image_search_tool = SerperDevTool(
    search_url="https://google.serper.dev/images",
    n_results=3,
)

image_downloader_tool = ImagesDownloader()
google_drive_uploader_tool = GoogleDriveUploader()

@CrewBase
class HistoryResearchAssistantCrew():
	"""HistoryResearchAssistant crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def image_finder(self) -> Agent:
		return Agent(
			config=self.agents_config['image_finder'],
			tools=[image_search_tool, image_downloader_tool, google_drive_uploader_tool],
			verbose=True
		)
	
	@task
	def image_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['image_research_task'],
			agent=self.image_finder(),
			tools=[image_downloader_tool, image_search_tool, google_drive_uploader_tool],
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the HistoryResearchAssistant crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)