#!/usr/bin/env python
import sys
import os
import argparse
import random
import logging
from dotenv import load_dotenv

from typing import List

from researcher.crew import ResearcherCrew

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def run(topics: List[str] | None = None):
    """
    Run the researcher crew.
    """

    if not topics:
        # Parse topic from command line args
        parser = argparse.ArgumentParser()
        parser.add_argument("--topics-filepath", type=str, help="A file path to a plaintext file with the research topics.")
        args = parser.parse_args()

        # Randomly pick a topic from the list
        topics = open(args.topics_filepath, "r").readlines()
        idx = random.randint(0, len(topics))
        topic = topics[idx]

        logger.info(f"Researching {topic}...")

        inputs = {'topic': topic}

        ResearcherCrew().crew().kickoff(inputs=inputs)


if __name__=="__main__":
    run()