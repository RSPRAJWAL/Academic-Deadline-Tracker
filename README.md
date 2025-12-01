# 📚 Academic Deadline Tracker

![GitHub License](https://img.shields.io/github/license/RSPRAJWAL/Academic-Deadline-Tracker)
![Last Commit](https://img.shields.io/github/last-commit/RSPRAJWAL/Academic-Deadline-Tracker)
![Repo Size](https://img.shields.io/github/repo-size/RSPRAJWAL/Academic-Deadline-Tracker)
![Issues](https://img.shields.io/github/issues/RSPRAJWAL/Academic-Deadline-Tracker)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![GitHub stars](https://img.shields.io/github/stars/RSPRAJWAL/Academic-Deadline-Tracker?style=social)

---

A modern, user-friendly productivity app designed to help students track projects, assignments, and exam deadlines with automation, countdowns, notifications, and smart reminders — all in one place.

---

## ✨ Key Features

- 📝 Create, edit, and delete academic tasks  
- ⏳ Smart countdown showing days left until deadline  
- 🔍 Search and filter by subject or priority  
- ✔️ Mark tasks as completed with archive history  
- 📤 Export / 📥 Import tasks as JSON  
- 🔔 Push notifications (Firebase) + local fallback  
- 🌓 Dark mode support  
- 📅 Calendar month view  
- 💾 SQLite storage with optional cloud configurations  

---

## 🛠️ Requirements

- **Python 3.10+**
- Dependencies listed in the project:
   

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
