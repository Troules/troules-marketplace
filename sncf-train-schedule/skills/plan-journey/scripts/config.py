"""
Shared token loading for SNCF scripts.

Priority:
  1. NAVITIA_API_TOKEN env var (already set)
  2. .claude/sncf-train-schedule.local.md (persistent, survives plugin updates)
  3. .env file via python-dotenv
"""
import os


def load_token():
    """Load NAVITIA_API_TOKEN into the environment if not already set."""
    if os.getenv("NAVITIA_API_TOKEN"):
        return

    # Try .claude/sncf-train-schedule.local.md in the working directory
    settings_file = os.path.join(os.getcwd(), ".claude", "sncf-train-schedule.local.md")
    if os.path.isfile(settings_file):
        with open(settings_file) as f:
            for line in f:
                if line.startswith("navitia_api_token:"):
                    token = line.split(":", 1)[1].strip().strip("'\"")
                    if token:
                        os.environ["NAVITIA_API_TOKEN"] = token
                    return

    # Fall back to .env via python-dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
