"""
LangSmith Observability Configuration for AI Medical Research Agent
Consolidated configuration for all observability settings
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()

# LangSmith Configuration
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "ai-medical-research-agent")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")

# Evaluation thresholds (migrated from observability_config.py)
MIN_RELEVANCE_SCORE = 0.3
MAX_PROCESSING_TIME = 30.0
MIN_CITATIONS = 1

# Basic logging configuration (migrated from observability_simple.py)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('medical_agent')

def setup_langsmith():
    """Setup LangSmith environment variables for tracing"""
    if LANGSMITH_API_KEY:
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
        os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
        os.environ["LANGSMITH_ENDPOINT"] = LANGSMITH_ENDPOINT
        print(f"✅ LangSmith tracing enabled for project: {LANGSMITH_PROJECT}")
        return True
    else:
        print("⚠️  LangSmith API key not found. Add LANGSMITH_API_KEY to your .env file")
        print("   You can get an API key from: https://smith.langchain.com/")
        return False

def get_project_url():
    """Get the LangSmith project URL for viewing traces"""
    if LANGSMITH_API_KEY and LANGSMITH_PROJECT:
        return f"https://smith.langchain.com/projects/{LANGSMITH_PROJECT}"
    return None

def log_info(message: str):
    """Simple info logging"""
    logger.info(message)

def log_error(message: str, error: Exception = None):
    """Simple error logging"""
    if error:
        logger.error(f"{message}: {str(error)}")
    else:
        logger.error(message)

def print_observability_info():
    """Print information about observability setup"""
    trace_url = get_project_url()
    if trace_url:
        print(f"\n📊 Observability Dashboard: {trace_url}")
        print("🔍 All queries, evaluations, and performance metrics are tracked in LangSmith")
    else:
        print("\n⚠️  LangSmith not configured. Set LANGSMITH_API_KEY in your .env file")

# Setup instructions for .env file
ENV_TEMPLATE = """
# LangSmith Configuration
# Get your API key from: https://smith.langchain.com/
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=ai-medical-research-agent

# OpenAI Configuration (required for the medical agent)
OPENAI_API_KEY=your_openai_api_key_here
"""

if __name__ == "__main__":
    print("🔧 LangSmith Configuration Check")
    print("=" * 40)
    
    success = setup_langsmith()
    
    if success:
        project_url = get_project_url()
        print(f"🌐 View traces at: {project_url}")
    else:
        print("\n📝 Add the following to your .env file:")
        print(ENV_TEMPLATE)