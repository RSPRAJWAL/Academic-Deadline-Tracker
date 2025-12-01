"""
Unit tests for the utils module.
"""
import unittest
from datetime import datetime, timedelta

from utils import format_countdown, calculate_reminder_time, parse_datetime


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_format_countdown_future_days(self):
        """Test formatting countdown with days in the future."""
        # Create a due date 5 days in the future
        future_date = datetime.now() + timedelta(days=5)
        due_date_str = future_date.isoformat()
        
        result = format_countdown(due_date_str)
        self.assertIn("days", result)
        self.assertIn("left", result)
    
    def test_format_countdown_future_hours(self):
        """Test formatting countdown with hours in the future."""
        # Create a due date 3 hours in the future
        future_date = datetime.now() + timedelta(hours=3)
        due_date_str = future_date.isoformat()
        
        result = format_countdown(due_date_str)
        self.assertIn("hours", result)
        self.assertIn("left", result)
    
    def test_format_countdown_future_minutes(self):
        """Test formatting countdown with minutes in the future."""
        # Create a due date 30 minutes in the future
        future_date = datetime.now() + timedelta(minutes=30)
        due_date_str = future_date.isoformat()
        
        result = format_countdown(due_date_str)
        self.assertIn("minutes", result)
        self.assertIn("left", result)
    
    def test_format_countdown_overdue(self):
        """Test formatting countdown for overdue tasks."""
        # Create a due date in the past
        past_date = datetime.now() - timedelta(days=2)
        due_date_str = past_date.isoformat()
        
        result = format_countdown(due_date_str)
        self.assertEqual(result, "OVERDUE")
    
    def test_format_countdown_invalid_date(self):
        """Test formatting countdown with invalid date string."""
        result = format_countdown("invalid-date")
        self.assertEqual(result, "Invalid date")
    
    def test_calculate_reminder_time_hours(self):
        """Test calculating reminder time with hours offset."""
        due_date = datetime.now() + timedelta(days=2)
        due_date_str = due_date.isoformat()
        
        reminder_time_str = calculate_reminder_time(due_date_str, "48 hours")
        self.assertIsNotNone(reminder_time_str)
        
        reminder_time = datetime.fromisoformat(reminder_time_str)
        expected_reminder = due_date - timedelta(hours=48)
        self.assertAlmostEqual(
            reminder_time.timestamp(),
            expected_reminder.timestamp(),
            delta=1  # Allow 1 second difference
        )
    
    def test_calculate_reminder_time_days(self):
        """Test calculating reminder time with days offset."""
        due_date = datetime.now() + timedelta(days=7)
        due_date_str = due_date.isoformat()
        
        reminder_time_str = calculate_reminder_time(due_date_str, "3 days")
        self.assertIsNotNone(reminder_time_str)
        
        reminder_time = datetime.fromisoformat(reminder_time_str)
        expected_reminder = due_date - timedelta(days=3)
        self.assertAlmostEqual(
            reminder_time.timestamp(),
            expected_reminder.timestamp(),
            delta=1  # Allow 1 second difference
        )
    
    def test_calculate_reminder_time_minutes(self):
        """Test calculating reminder time with minutes offset."""
        due_date = datetime.now() + timedelta(hours=2)
        due_date_str = due_date.isoformat()
        
        reminder_time_str = calculate_reminder_time(due_date_str, "30 minutes")
        self.assertIsNotNone(reminder_time_str)
        
        reminder_time = datetime.fromisoformat(reminder_time_str)
        expected_reminder = due_date - timedelta(minutes=30)
        self.assertAlmostEqual(
            reminder_time.timestamp(),
            expected_reminder.timestamp(),
            delta=1  # Allow 1 second difference
        )
    
    def test_calculate_reminder_time_invalid_offset(self):
        """Test calculating reminder time with invalid offset."""
        due_date = datetime.now() + timedelta(days=2)
        due_date_str = due_date.isoformat()
        
        # Test invalid format
        result = calculate_reminder_time(due_date_str, "invalid")
        self.assertIsNone(result)
        
        # Test empty offset
        result = calculate_reminder_time(due_date_str, "")
        self.assertIsNone(result)
    
    def test_parse_datetime(self):
        """Test parsing date and time strings."""
        date_str = "2025-10-20"
        time_str = "23:59"
        
        result = parse_datetime(date_str, time_str)
        self.assertEqual(result, "2025-10-20T23:59:00")
    
    def test_parse_datetime_invalid(self):
        """Test parsing invalid date/time strings."""
        result = parse_datetime("invalid", "23:59")
        self.assertEqual(result, "")
        
        result = parse_datetime("2025-10-20", "invalid")
        self.assertEqual(result, "")


if __name__ == '__main__':
    unittest.main()