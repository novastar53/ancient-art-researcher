#!/usr/bin/env python
import sys
from researcher.crew import ResearcherCrew

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Palm leaf manuscript bihar buddhist'
    }
    ResearcherCrew().crew().kickoff(inputs=inputs)


if __name__=="__main__":
    run()