#!/usr/bin/env python
import sys
import os
from dotenv import load_dotenv

from researcher.crew import ResearcherCrew

load_dotenv()

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Art by Kshitindranath Majumdar'
    }
    ResearcherCrew().crew().kickoff(inputs=inputs)


if __name__=="__main__":
    run()