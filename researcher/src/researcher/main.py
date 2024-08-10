#!/usr/bin/env python
import sys
import os
import argparse
from dotenv import load_dotenv

from researcher.crew import ResearcherCrew

load_dotenv()

def run():
    """
    Run the researcher crew.
    """

    # Parse topic 
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", type=str, help="Research Topic")
    args = parser.parse_args()
    inputs = {'topic': args.topic}

    ResearcherCrew().crew().kickoff(inputs=inputs)

