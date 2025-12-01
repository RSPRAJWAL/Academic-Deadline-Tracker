# Academic Deadline Tracker

A simple, user-friendly desktop application for students to track assignments, projects, and exam deadlines with countdowns and notifications.

## Features

- Add, edit, delete tasks with title, description, due date, course/subject, priority, and reminder time
- List view sorted by nearest due date with human-friendly countdowns
- Search and filter by course/subject and priority
- Mark tasks as completed with archived view
- Export and import tasks as JSON
- Push notifications via Firebase Cloud Messaging with local fallback
- Dark mode toggle
- Calendar month view
- SQLite database storage with JSON backup

## Requirements

- Python 3.10+
- Dependencies listed in [requirements.txt](requirements.txt)

## Setup

1. Clone or download this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

## Firebase Configuration

To enable push notifications:

1. Create a Firebase project at https://console.firebase.google.com/
2. Download your service account key as `firebase_config.json`
3. Place the file in the application directory
4. Enable notifications in Settings

## Files

- `main.py` - Entry point
- `ui.py` - GUI implementation
- `models.py` - Data models and database logic
- `notifications.py` - Notification handling
- `utils.py` - Helper functions
- `tests/` - Unit tests
- `sample_firebase_config_template.json` - Firebase configuration template