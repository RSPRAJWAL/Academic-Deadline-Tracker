"""
Notification system for the Academic Deadline Tracker.
Handles both Firebase Cloud Messaging and local notifications.
"""
import os
import json
import threading
import time
from datetime import datetime
from typing import Optional, Dict, Any

try:
    from plyer import notification as plyer_notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False
    print("Plyer not available, local notifications disabled")

try:
    import firebase_admin
    from firebase_admin import messaging
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("Firebase Admin SDK not available, FCM notifications disabled")


class NotificationManager:
    """Manages sending notifications via Firebase or local system."""
    
    def __init__(self, config_file: str = "firebase_config.json"):
        self.config_file = config_file
        self.firebase_enabled = False
        self.local_enabled = True
        self._initialize_firebase()
        self.scheduled_notifications = {}
        self.notification_thread = None
        self.running = False
    
    def _initialize_firebase(self) -> None:
        """Initialize Firebase if config file exists and library is available."""
        if not FIREBASE_AVAILABLE:
            return
            
        if os.path.exists(self.config_file):
            try:
                # Initialize Firebase only if not already initialized
                if not firebase_admin._apps:
                    firebase_admin.initialize_app()
                self.firebase_enabled = True
                print("Firebase initialized successfully")
            except Exception as e:
                print(f"Failed to initialize Firebase: {e}")
                self.firebase_enabled = False
        else:
            print("Firebase config file not found, FCM disabled")
    
    def send_fcm_notification(self, title: str, body: str, token: str) -> bool:
        """
        Send a notification via Firebase Cloud Messaging.
        
        Args:
            title: Notification title
            body: Notification body
            token: Device registration token
            
        Returns:
            True if successful, False otherwise
        """
        if not self.firebase_enabled or not FIREBASE_AVAILABLE:
            return False
            
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                token=token
            )
            response = messaging.send(message)
            print(f"Successfully sent FCM message: {response}")
            return True
        except Exception as e:
            print(f"Failed to send FCM notification: {e}")
            return False
    
    def send_local_notification(self, title: str, body: str) -> bool:
        """
        Send a local desktop notification.
        
        Args:
            title: Notification title
            body: Notification body
            
        Returns:
            True if successful, False otherwise
        """
        if not self.local_enabled or not PLYER_AVAILABLE:
            return False
            
        try:
            plyer_notification.notify(
                title=title,
                message=body,
                app_name="Academic Deadline Tracker",
                timeout=10
            )
            return True
        except Exception as e:
            print(f"Failed to send local notification: {e}")
            return False
    
    def send_notification(self, title: str, body: str, token: Optional[str] = None) -> None:
        """
        Send notification via Firebase (if enabled and token provided) or fallback to local.
        
        Args:
            title: Notification title
            body: Notification body
            token: Optional Firebase device token
        """
        # Try Firebase first if enabled and token provided
        if self.firebase_enabled and token:
            if self.send_fcm_notification(title, body, token):
                return
        
        # Fallback to local notification
        self.send_local_notification(title, body)
    
    def schedule_notification(self, task_id: int, reminder_time_str: str, title: str, body: str) -> None:
        """
        Schedule a notification for a specific time.
        
        Args:
            task_id: Task identifier
            reminder_time_str: ISO format datetime string
            title: Notification title
            body: Notification body
        """
        try:
            reminder_time = datetime.fromisoformat(reminder_time_str)
            self.scheduled_notifications[task_id] = {
                'time': reminder_time,
                'title': title,
                'body': body
            }
            
            # Start notification thread if not already running
            if not self.running:
                self.start_notification_service()
        except ValueError:
            print(f"Invalid reminder time format: {reminder_time_str}")
    
    def cancel_scheduled_notification(self, task_id: int) -> None:
        """
        Cancel a scheduled notification.
        
        Args:
            task_id: Task identifier
        """
        self.scheduled_notifications.pop(task_id, None)
    
    def start_notification_service(self) -> None:
        """Start the background notification service."""
        if self.running:
            return
            
        self.running = True
        self.notification_thread = threading.Thread(target=self._notification_worker, daemon=True)
        self.notification_thread.start()
        print("Notification service started")
    
    def stop_notification_service(self) -> None:
        """Stop the background notification service."""
        self.running = False
        if self.notification_thread:
            self.notification_thread.join()
        print("Notification service stopped")
    
    def _notification_worker(self) -> None:
        """Background worker that checks for due notifications."""
        while self.running:
            now = datetime.now()
            due_notifications = []
            
            # Check for due notifications
            for task_id, notification_data in list(self.scheduled_notifications.items()):
                if notification_data['time'] <= now:
                    due_notifications.append((task_id, notification_data))
            
            # Send due notifications
            for task_id, notification_data in due_notifications:
                self.send_local_notification(
                    notification_data['title'],
                    notification_data['body']
                )
                # Remove sent notification
                self.scheduled_notifications.pop(task_id, None)
            
            # Sleep for a minute before checking again
            time.sleep(60)