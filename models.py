"""
Data models and database logic for the Academic Deadline Tracker.
"""
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class Task:
    """Represents a task with all its attributes."""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    due_date: str = ""  # ISO format datetime string
    course: str = ""
    priority: str = "medium"  # low, medium, high
    reminder_time: Optional[str] = None  # ISO format datetime string
    completed: bool = False
    created_at: str = ""  # ISO format datetime string

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create task from dictionary."""
        return cls(**data)


class DatabaseManager:
    """Manages SQLite database operations for tasks."""
    
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self) -> None:
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT NOT NULL,
                    course TEXT,
                    priority TEXT DEFAULT 'medium',
                    reminder_time TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()
    
    def add_task(self, task: Task) -> int:
        """Add a new task to the database."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (title, description, due_date, course, priority, reminder_time, completed, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.title,
                task.description,
                task.due_date,
                task.course,
                task.priority,
                task.reminder_time,
                task.completed,
                task.created_at
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def update_task(self, task: Task) -> None:
        """Update an existing task."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks SET
                    title = ?, description = ?, due_date = ?, course = ?,
                    priority = ?, reminder_time = ?, completed = ?
                WHERE id = ?
            """, (
                task.title,
                task.description,
                task.due_date,
                task.course,
                task.priority,
                task.reminder_time,
                task.completed,
                task.id
            ))
            conn.commit()
        finally:
            conn.close()
    
    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
        finally:
            conn.close()
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row:
                return Task(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    due_date=row[3],
                    course=row[4],
                    priority=row[5],
                    reminder_time=row[6],
                    completed=bool(row[7]),
                    created_at=row[8]
                )
            return None
        finally:
            conn.close()
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks ORDER BY due_date ASC")
            rows = cursor.fetchall()
            return [
                Task(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    due_date=row[3],
                    course=row[4],
                    priority=row[5],
                    reminder_time=row[6],
                    completed=bool(row[7]),
                    created_at=row[8]
                )
                for row in rows
            ]
        finally:
            conn.close()
    
    def get_pending_tasks(self) -> List[Task]:
        """Retrieve all pending (not completed) tasks."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE completed = 0 ORDER BY due_date ASC")
            rows = cursor.fetchall()
            return [
                Task(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    due_date=row[3],
                    course=row[4],
                    priority=row[5],
                    reminder_time=row[6],
                    completed=bool(row[7]),
                    created_at=row[8]
                )
                for row in rows
            ]
        finally:
            conn.close()
    
    def get_completed_tasks(self) -> List[Task]:
        """Retrieve all completed tasks."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE completed = 1 ORDER BY due_date ASC")
            rows = cursor.fetchall()
            return [
                Task(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    due_date=row[3],
                    course=row[4],
                    priority=row[5],
                    reminder_time=row[6],
                    completed=bool(row[7]),
                    created_at=row[8]
                )
                for row in rows
            ]
        finally:
            conn.close()
    
    def export_tasks(self, filepath: str) -> None:
        """Export all tasks to a JSON file."""
        tasks = self.get_all_tasks()
        task_dicts = [task.to_dict() for task in tasks]
        with open(filepath, 'w') as f:
            json.dump(task_dicts, f, indent=2)
    
    def import_tasks(self, filepath: str) -> None:
        """Import tasks from a JSON file."""
        with open(filepath, 'r') as f:
            task_dicts = json.load(f)
        
        for task_dict in task_dicts:
            # Remove id to allow creation of new records
            task_dict.pop('id', None)
            task = Task.from_dict(task_dict)
            self.add_task(task)