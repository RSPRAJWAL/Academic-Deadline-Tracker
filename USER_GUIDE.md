# User Guide

## Installation

1. Make sure you have Python 3.10 or higher installed
2. Download or clone the Academic Deadline Tracker repository
3. Run the installation script:
   - On Windows: Double-click `install.bat` or run `install.bat` in Command Prompt
   - On macOS/Linux: Run `./install.sh` in Terminal
4. Alternatively, you can manually install dependencies with:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Run the application:
   - On Windows: Double-click `run.bat` or run `run.bat` in Command Prompt
   - On macOS/Linux: Run `./run.sh` in Terminal
2. Alternatively, you can run directly with:
   ```
   python main.py
   ```

## Getting Started

When you first run the application, you'll see an empty task list. Here's how to get started:

### Adding a Task

1. Click the "Add Task" button in the top right corner
2. Fill in the task details:
   - **Title**: A short name for the task
   - **Description**: Detailed information about the task
   - **Course**: The subject or course the task belongs to
   - **Priority**: Low, Medium, or High
   - **Due Date**: The date the task is due
   - **Due Time**: The time the task is due
   - **Reminder**: Optional reminder time (e.g., "48 hours", "30 minutes")
3. Click "Save" to add the task

### Viewing Tasks

Tasks are displayed in the main list, sorted by due date (nearest first). Each task shows:
- Title
- Course
- Due date
- Priority
- Countdown to due date

### Filtering Tasks

Use the sidebar to filter tasks:
- **Course**: Show only tasks for a specific course
- **Priority**: Show only tasks with a specific priority level
- **Status**: Show pending, completed, or all tasks

### Editing a Task

1. Select a task by clicking on it
2. Click the "Edit" button
3. Make your changes
4. Click "Save"

### Completing a Task

1. Select a task by clicking on it
2. Click the "Mark Complete" button
3. Completed tasks will be moved to the "Completed" filter

### Deleting a Task

1. Select a task by clicking on it
2. Click the "Delete" button
3. Confirm deletion

### Exporting Tasks

1. Click "Export Tasks" in the sidebar
2. Choose a location and filename
3. Tasks will be saved as a JSON file

### Importing Tasks

1. Click "Import Tasks" in the sidebar
2. Select a JSON file with tasks
3. Tasks will be added to your current list

## Notifications

The application can send reminders for tasks with reminder times set:

1. **Local Notifications**: Default notification method using your operating system's notification system
2. **Firebase Cloud Messaging**: Optional push notifications (requires Firebase setup)

### Setting up Firebase (Optional)

1. Create a Firebase project at https://console.firebase.google.com/
2. Download your service account key as `firebase_config.json`
3. Place the file in the application directory
4. Enable notifications in Settings (when implemented)

## Settings

The application includes several settings (to be implemented):
- Dark mode toggle
- Default reminder time
- Notification preferences
- Firebase configuration

## Calendar View

The calendar view (to be implemented) will show tasks on a monthly calendar for better visualization.

## Troubleshooting

### Common Issues

1. **Application won't start**: Make sure you've installed all dependencies with `pip install -r requirements.txt`
2. **Notifications not working**: Ensure your operating system allows notifications for Python applications
3. **Database errors**: Try deleting the `tasks.db` file and restarting the application (this will clear all data)

### Getting Help

If you encounter issues not covered in this guide:
1. Check the README.md file for additional information
2. Review the project documentation
3. Submit an issue on the project's GitHub repository