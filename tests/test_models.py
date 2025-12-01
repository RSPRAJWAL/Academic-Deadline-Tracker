import unittest
import tempfile
import os
import sqlite3
import time
from datetime import datetime, timedelta

from models import Task, DatabaseManager


class TestTask(unittest.TestCase):
    """Test cases for the Task dataclass."""
    
    def test_task_creation(self):
        """Test creating a task with all attributes."""
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            due_date="2025-12-31T23:59:59",
            course="Mathematics",
            priority="high",
            reminder_time="2025-12-30T23:59:59",
            completed=False,
            created_at="2025-01-01T00:00:00"
        )
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.due_date, "2025-12-31T23:59:59")
        self.assertEqual(task.course, "Mathematics")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.reminder_time, "2025-12-30T23:59:59")
        self.assertFalse(task.completed)
        self.assertEqual(task.created_at, "2025-01-01T00:00:00")
    
    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            due_date="2025-12-31T23:59:59",
            course="Mathematics",
            priority="high",
            reminder_time="2025-12-30T23:59:59",
            completed=False,
            created_at="2025-01-01T00:00:00"
        )
        
        task_dict = task.to_dict()
        self.assertIsInstance(task_dict, dict)
        self.assertEqual(task_dict['id'], 1)
        self.assertEqual(task_dict['title'], "Test Task")
    
    def test_task_from_dict(self):
        """Test creating task from dictionary."""
        task_dict = {
            'id': 1,
            'title': "Test Task",
            'description': "Test Description",
            'due_date': "2025-12-31T23:59:59",
            'course': "Mathematics",
            'priority': "high",
            'reminder_time': "2025-12-30T23:59:59",
            'completed': False,
            'created_at': "2025-01-01T00:00:00"
        }
        
        task = Task.from_dict(task_dict)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")


class TestDatabaseManager(unittest.TestCase):
    """Test cases for the DatabaseManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary database for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_file.close()
        self.db_path = self.temp_file.name
        self.db = DatabaseManager(self.db_path)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up the temporary database
        if os.path.exists(self.db_path):
            # On Windows, we might need to wait for the file to be released
            for _ in range(10):  # Try up to 10 times
                try:
                    os.unlink(self.db_path)
                    break
                except PermissionError:
                    time.sleep(0.1)  # Wait 100ms before trying again
    
    def test_init_database(self):
        """Test database initialization."""
        # Database should be initialized with tasks table
        tasks = self.db.get_all_tasks()
        self.assertIsInstance(tasks, list)
        self.assertEqual(len(tasks), 0)
    
    def test_add_task(self):
        """Test adding a task to the database."""
        task = Task(
            title="Test Task",
            description="Test Description",
            due_date="2025-12-31T23:59:59",
            course="Mathematics",
            priority="high",
            created_at="2025-01-01T00:00:00"
        )
        
        task_id = self.db.add_task(task)
        self.assertIsInstance(task_id, int)
        self.assertGreater(task_id, 0)
    
    def test_get_task(self):
        """Test retrieving a task from the database."""
        # Add a task first
        task = Task(
            title="Test Task",
            description="Test Description",
            due_date="2025-12-31T23:59:59",
            course="Mathematics",
            priority="high",
            created_at="2025-01-01T00:00:00"
        )
        
        task_id = self.db.add_task(task)
        
        # Retrieve the task
        retrieved_task = self.db.get_task(task_id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.id, task_id)
        self.assertEqual(retrieved_task.title, "Test Task")
    
    def test_update_task(self):
        """Test updating a task in the database."""
        # Add a task first
        task = Task(
            title="Test Task",
            description="Test Description",
            due_date="2025-12-31T23:59:59",
            course="Mathematics",
            priority="high",
            created_at="2025-01-01T00:00:00"
        )
        
        task_id = self.db.add_task(task)
        
        # Update the task
        task.id = task_id  # Make sure the task has the correct ID
        task.title = "Updated Task"
        task.completed = True
        self.db.update_task(task)
        
        # Retrieve the updated task
        updated_task = self.db.get_task(task_id)
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertTrue(updated_task.completed)
    
    def test_delete_task(self):
        """Test deleting a task from the database."""
        # Add a task first
        task = Task(
            title="Test Task",
            description="Test Description",
            due_date="2025-12-31T23:59:59",
            course="Mathematics",
            priority="high",
            created_at="2025-01-01T00:00:00"
        )
        
        task_id = self.db.add_task(task)
        
        # Verify task exists
        retrieved_task = self.db.get_task(task_id)
        self.assertIsNotNone(retrieved_task)
        
        # Delete the task
        self.db.delete_task(task_id)
        
        # Verify task no longer exists
        deleted_task = self.db.get_task(task_id)
        self.assertIsNone(deleted_task)
    
    def test_get_all_tasks(self):
        """Test retrieving all tasks from the database."""
        # Add multiple tasks
        for i in range(3):
            task = Task(
                title=f"Test Task {i}",
                description=f"Test Description {i}",
                due_date="2025-12-31T23:59:59",
                course="Mathematics",
                priority="high",
                created_at="2025-01-01T00:00:00"
            )
            self.db.add_task(task)
        
        # Retrieve all tasks
        tasks = self.db.get_all_tasks()
        self.assertEqual(len(tasks), 3)
    
    def test_get_pending_tasks(self):
        """Test retrieving pending tasks from the database."""
        # Add completed and pending tasks
        for i in range(3):
            task = Task(
                title=f"Pending Task {i}",
                description=f"Test Description {i}",
                due_date="2025-12-31T23:59:59",
                course="Mathematics",
                priority="high",
                completed=False,
                created_at="2025-01-01T00:00:00"
            )
            self.db.add_task(task)
        
        for i in range(2):
            task = Task(
                title=f"Completed Task {i}",
                description=f"Test Description {i}",
                due_date="2025-12-31T23:59:59",
                course="Mathematics",
                priority="high",
                completed=True,
                created_at="2025-01-01T00:00:00"
            )
            self.db.add_task(task)
        
        # Retrieve pending tasks
        pending_tasks = self.db.get_pending_tasks()
        self.assertEqual(len(pending_tasks), 3)
        for task in pending_tasks:
            self.assertFalse(task.completed)
    
    def test_get_completed_tasks(self):
        """Test retrieving completed tasks from the database."""
        # Add completed and pending tasks
        for i in range(3):
            task = Task(
                title=f"Pending Task {i}",
                description=f"Test Description {i}",
                due_date="2025-12-31T23:59:59",
                course="Mathematics",
                priority="high",
                completed=False,
                created_at="2025-01-01T00:00:00"
            )
            self.db.add_task(task)
        
        for i in range(2):
            task = Task(
                title=f"Completed Task {i}",
                description=f"Test Description {i}",
                due_date="2025-12-31T23:59:59",
                course="Mathematics",
                priority="high",
                completed=True,
                created_at="2025-01-01T00:00:00"
            )
            self.db.add_task(task)
        
        # Retrieve completed tasks
        completed_tasks = self.db.get_completed_tasks()
        self.assertEqual(len(completed_tasks), 2)
        for task in completed_tasks:
            self.assertTrue(task.completed)


if __name__ == '__main__':
    unittest.main()