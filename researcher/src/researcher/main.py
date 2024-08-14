#!/usr/bin/env python
import sys
import os
import argparse
from dotenv import load_dotenv

from researcher.crew import ResearcherCrew

load_dotenv()

def run(topic: str | None = None):
    """
    Run the researcher crew.
    """

    if not topic:
        # Parse topic from command line args
        parser = argparse.ArgumentParser()
        parser.add_argument("--topic", type=str, help="Research Topic")
        args = parser.parse_args()
        topic = args.topic

    inputs = {'topic': topic}

    ResearcherCrew().crew().kickoff(inputs=inputs)


if __name__=="__main__":
    run()