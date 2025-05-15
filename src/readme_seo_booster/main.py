#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
import argparse
from readme_seo_booster.crew import ReadmeSeoBooster
import os
from dotenv import load_dotenv
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
# execution : crewai run --repo MeirKaD/SBR-MCP

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="README SEO Booster")
    parser.add_argument("--repo", required=True, help="GitHub repository in format username/project")
    parser.add_argument("--model", default="gpt-4o-mini", help="gemini model to use")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    return parser.parse_args()

def validate_env():
    """Validate environment variables"""
    required_vars = ["GEMINI_API_KEY", "BRIGHTDATA_API_TOKEN", "GITHUB_PAT"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        print("Please set them in your .env file")
        sys.exit(1)

def run():
    """Run the README SEO Booster crew"""
    load_dotenv()
    
    inputs = {
        "repo_name": "MeirKaD/MCP_ADK",
        "current_date": datetime.now().strftime("%Y%m%d")
    }
    
    try:
        crew = ReadmeSeoBooster()
        result = crew.crew().kickoff(inputs=inputs)
        print(result)
    except Exception as e:
        print(f"Error running crew: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()