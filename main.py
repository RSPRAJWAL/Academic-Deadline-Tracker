"""
Main entry point for the Academic Deadline Tracker application.
"""
import sys
import os

# Add the current directory to the Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui import main

if __name__ == "__main__":
    main()