# Project Structure

```
AcademicDeadlineTracker/
├── main.py                 # Entry point
├── ui.py                   # GUI implementation
├── models.py               # Data models and database logic
├── notifications.py        # Notification system
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── setup.py                # Setup script
├── README.md               # Project documentation
├── PROJECT_STRUCTURE.md    # This file
├── sample_firebase_config_template.json  # Firebase config template
├── run.bat                 # Windows run script
├── run.sh                  # Unix run script
├── install.bat             # Windows install script
├── install.sh              # Unix install script
├── tasks.db               # SQLite database (created on first run)
└── tests/
    ├── __init__.py         # Package init
    ├── test_models.py      # Tests for models
    ├── test_utils.py       # Tests for utilities
    └── run_tests.py        # Test runner
```

## File Descriptions

### Core Application Files

- **main.py**: Entry point that initializes and runs the application
- **ui.py**: Implements the graphical user interface using Tkinter
- **models.py**: Contains data models (Task) and database management (DatabaseManager)
- **notifications.py**: Handles both Firebase Cloud Messaging and local notifications
- **utils.py**: Utility functions for date formatting, parsing, and calculations

### Configuration and Setup

- **requirements.txt**: Lists all Python dependencies required for the application
- **setup.py**: Standard Python setup script for packaging
- **README.md**: Comprehensive documentation for users and developers
- **sample_firebase_config_template.json**: Template for Firebase configuration

### Scripts

- **run.bat / run.sh**: Platform-specific scripts to run the application
- **install.bat / install.sh**: Platform-specific scripts to install dependencies

### Testing

- **tests/**: Directory containing all unit tests
- **tests/test_models.py**: Tests for data models and database operations
- **tests/test_utils.py**: Tests for utility functions
- **tests/run_tests.py**: Script to run all tests

## Database

The application uses SQLite for local data storage. The database file (`tasks.db`) is automatically created when the application first runs.

## Data Flow

1. User interacts with the GUI (ui.py)
2. UI calls methods in models.py to manipulate data
3. models.py handles all database operations
4. notifications.py handles sending reminders
5. utils.py provides helper functions for date/time operations