"""
Utility functions for the Academic Deadline Tracker.
"""
from datetime import datetime, timedelta
from typing import Optional


def format_countdown(due_date_str: str) -> str:
    """
    Format a human-friendly countdown string from a due date.
    
    Args:
        due_date_str: ISO format datetime string
        
    Returns:
        Formatted countdown string (e.g., "2 days, 4 hours left")
    """
    try:
        due_date = datetime.fromisoformat(due_date_str)
        now = datetime.now()
        diff = due_date - now
        
        if diff.total_seconds() < 0:
            return "OVERDUE"
        
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0 and days == 0:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        
        if not parts:
            return "Due soon"
        
        return ", ".join(parts) + " left"
    except ValueError:
        return "Invalid date"


def calculate_reminder_time(due_date_str: str, reminder_offset: str) -> Optional[str]:
    """
    Calculate the reminder time based on due date and offset.
    
    Args:
        due_date_str: ISO format datetime string
        reminder_offset: Reminder offset (e.g., "48 hours", "30 minutes")
        
    Returns:
        ISO format datetime string for reminder time or None if invalid
    """
    try:
        due_date = datetime.fromisoformat(due_date_str)
        
        if not reminder_offset:
            return None
            
        # Parse reminder offset
        parts = reminder_offset.strip().split()
        if len(parts) != 2:
            return None
            
        value = int(parts[0])
        unit = parts[1].lower()
        
        if unit.startswith('minute'):
            reminder_time = due_date - timedelta(minutes=value)
        elif unit.startswith('hour'):
            reminder_time = due_date - timedelta(hours=value)
        elif unit.startswith('day'):
            reminder_time = due_date - timedelta(days=value)
        else:
            return None
            
        return reminder_time.isoformat()
    except (ValueError, IndexError):
        return None


def parse_datetime(date_str: str, time_str: str) -> str:
    """
    Parse date and time strings into ISO format datetime.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        time_str: Time string in HH:MM format
        
    Returns:
        ISO format datetime string
    """
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        return dt.isoformat()
    except ValueError:
        return ""