"""
Main entry point for the Gemini agent system.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main entry point for the agent."""
    agent_type = os.getenv('AGENT_TYPE', 'main')
    
    print(f"Starting {agent_type} agent...")
    print(f"Gemini API Key configured: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
    print(f"Log Level: {os.getenv('LOG_LEVEL', 'INFO')}")
    
    # Agent initialization will go here
    print(f"{agent_type} agent is ready!")
    
    # Keep the container running
    import time
    try:
        while True:
            time.sleep(60)
            print(f"{agent_type} agent is running...")
    except KeyboardInterrupt:
        print(f"\nShutting down {agent_type} agent...")
        sys.exit(0)

if __name__ == "__main__":
    main()
