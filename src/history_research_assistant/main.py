#!/usr/bin/env python
import sys
from history_research_assistant.crew import HistoryResearchAssistantCrew

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Sculptures excavated from the Satvahana capital at Mansar'
    }
    HistoryResearchAssistantCrew().crew().kickoff(inputs=inputs)


if __name__=="__main__":
    run()