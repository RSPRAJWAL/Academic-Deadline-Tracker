"""
GUI implementation for the Academic Deadline Tracker using Tkinter.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import json
from typing import List, Optional

from models import Task, DatabaseManager
from utils import format_countdown, parse_datetime, calculate_reminder_time
from notifications import NotificationManager


class AcademicDeadlineTrackerUI:
    """Main UI class for the Academic Deadline Tracker."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Academic Deadline Tracker")
        self.root.geometry("1000x700")
        
        # Initialize components
        self.db = DatabaseManager()
        self.notification_manager = NotificationManager()
        self.current_tasks: List[Task] = []
        self.filtered_tasks: List[Task] = []
        self.dark_mode = False
        
        # Create UI
        self.create_widgets()
        self.load_tasks()
        self.update_task_list()
        
        # Start notification service
        self.notification_manager.start_notification_service()
    
    def create_widgets(self) -> None:
        """Create all UI widgets."""
        # Create main frames
        self.sidebar_frame = ttk.Frame(self.root, width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.detail_frame = ttk.Frame(self.root, width=300)
        self.detail_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content
        self.create_main_content()
        
        # Create detail panel
        self.create_detail_panel()
    
    def create_sidebar(self) -> None:
        """Create the sidebar with filters and controls."""
        # Dark mode toggle
        self.dark_mode_var = tk.BooleanVar()
        dark_mode_check = ttk.Checkbutton(
            self.sidebar_frame,
            text="Dark Mode",
            variable=self.dark_mode_var,
            command=self.toggle_dark_mode
        )
        dark_mode_check.pack(pady=5, anchor=tk.W)
        
        # Course filter
        ttk.Label(self.sidebar_frame, text="Filter by Course:").pack(pady=(10, 0), anchor=tk.W)
        self.course_filter_var = tk.StringVar()
        self.course_filter_combo = ttk.Combobox(
            self.sidebar_frame,
            textvariable=self.course_filter_var,
            state="readonly"
        )
        self.course_filter_combo.pack(fill=tk.X, pady=5)
        self.course_filter_combo.bind("<<ComboboxSelected>>", self.apply_filters)
        
        # Priority filter
        ttk.Label(self.sidebar_frame, text="Filter by Priority:").pack(pady=(10, 0), anchor=tk.W)
        self.priority_filter_var = tk.StringVar(value="All")
        self.priority_filter_combo = ttk.Combobox(
            self.sidebar_frame,
            textvariable=self.priority_filter_var,
            values=["All", "High", "Medium", "Low"],
            state="readonly"
        )
        self.priority_filter_combo.pack(fill=tk.X, pady=5)
        self.priority_filter_combo.bind("<<ComboboxSelected>>", self.apply_filters)
        
        # Status filter
        ttk.Label(self.sidebar_frame, text="Filter by Status:").pack(pady=(10, 0), anchor=tk.W)
        self.status_filter_var = tk.StringVar(value="Pending")
        self.status_filter_combo = ttk.Combobox(
            self.sidebar_frame,
            textvariable=self.status_filter_var,
            values=["Pending", "Completed", "All"],
            state="readonly"
        )
        self.status_filter_combo.pack(fill=tk.X, pady=5)
        self.status_filter_combo.bind("<<ComboboxSelected>>", self.apply_filters)
        
        # Filter buttons
        ttk.Button(
            self.sidebar_frame,
            text="Apply Filters",
            command=self.apply_filters
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            self.sidebar_frame,
            text="Clear Filters",
            command=self.clear_filters
        ).pack(fill=tk.X, pady=5)
        
        # Export/Import
        ttk.Button(
            self.sidebar_frame,
            text="Export Tasks",
            command=self.export_tasks
        ).pack(fill=tk.X, pady=(20, 5))
        
        ttk.Button(
            self.sidebar_frame,
            text="Import Tasks",
            command=self.import_tasks
        ).pack(fill=tk.X, pady=5)
        
        # Calendar view button
        ttk.Button(
            self.sidebar_frame,
            text="Calendar View",
            command=self.show_calendar_view
        ).pack(fill=tk.X, pady=(20, 5))
        
        # Settings button
        ttk.Button(
            self.sidebar_frame,
            text="Settings",
            command=self.show_settings
        ).pack(fill=tk.X, pady=5)
    
    def create_main_content(self) -> None:
        """Create the main content area with task list."""
        # Header with add button
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="Tasks", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        self.add_task_btn = ttk.Button(
            header_frame,
            text="Add Task",
            command=self.show_add_task_dialog
        )
        self.add_task_btn.pack(side=tk.RIGHT)
        
        # Task list
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with scrollbar
        self.task_tree = ttk.Treeview(
            list_frame,
            columns=("Title", "Course", "Due Date", "Priority", "Countdown"),
            show="headings"
        )
        
        # Define headings
        self.task_tree.heading("Title", text="Title")
        self.task_tree.heading("Course", text="Course")
        self.task_tree.heading("Due Date", text="Due Date")
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.heading("Countdown", text="Countdown")
        
        # Define column widths
        self.task_tree.column("Title", width=200)
        self.task_tree.column("Course", width=100)
        self.task_tree.column("Due Date", width=120)
        self.task_tree.column("Priority", width=80)
        self.task_tree.column("Countdown", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.task_tree.bind("<Double-1>", self.on_task_double_click)
    
    def create_detail_panel(self) -> None:
        """Create the detail panel for task information."""
        ttk.Label(self.detail_frame, text="Task Details", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        # Task details will be shown here when a task is selected
        self.detail_text = tk.Text(self.detail_frame, wrap=tk.WORD, height=20)
        self.detail_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Action buttons
        button_frame = ttk.Frame(self.detail_frame)
        button_frame.pack(fill=tk.X)
        
        self.edit_btn = ttk.Button(
            button_frame,
            text="Edit",
            command=self.show_edit_task_dialog,
            state=tk.DISABLED
        )
        self.edit_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.delete_btn = ttk.Button(
            button_frame,
            text="Delete",
            command=self.delete_selected_task,
            state=tk.DISABLED
        )
        self.delete_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        self.complete_btn = ttk.Button(
            button_frame,
            text="Mark Complete",
            command=self.complete_selected_task,
            state=tk.DISABLED
        )
        self.complete_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
    
    def load_tasks(self) -> None:
        """Load tasks from database."""
        self.current_tasks = self.db.get_all_tasks()
        self.update_course_filter()
    
    def update_course_filter(self) -> None:
        """Update the course filter dropdown with available courses."""
        courses = list(set(task.course for task in self.current_tasks if task.course))
        courses.insert(0, "All")
        self.course_filter_combo['values'] = courses
        if self.course_filter_var.get() not in courses:
            self.course_filter_var.set("All")
    
    def update_task_list(self) -> None:
        """Update the task list display."""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Add filtered tasks
        for task in self.filtered_tasks:
            countdown = format_countdown(task.due_date)
            priority = task.priority.capitalize()
            
            # Set tag based on priority for coloring
            tag = priority.lower()
            
            self.task_tree.insert(
                "",
                tk.END,
                values=(task.title, task.course, task.due_date, priority, countdown),
                tags=(tag,),
                iid=task.id
            )
        
        # Configure tags for coloring
        self.task_tree.tag_configure("high", background="#ffcccc")
        self.task_tree.tag_configure("medium", background="#fff2cc")
        self.task_tree.tag_configure("low", background="#d9ead3")
    
    def apply_filters(self, event=None) -> None:
        """Apply the selected filters to the task list."""
        course_filter = self.course_filter_var.get()
        priority_filter = self.priority_filter_var.get()
        status_filter = self.status_filter_var.get()
        
        self.filtered_tasks = self.current_tasks.copy()
        
        # Apply course filter
        if course_filter and course_filter != "All":
            self.filtered_tasks = [task for task in self.filtered_tasks if task.course == course_filter]
        
        # Apply priority filter
        if priority_filter and priority_filter != "All":
            self.filtered_tasks = [task for task in self.filtered_tasks if task.priority.lower() == priority_filter.lower()]
        
        # Apply status filter
        if status_filter == "Pending":
            self.filtered_tasks = [task for task in self.filtered_tasks if not task.completed]
        elif status_filter == "Completed":
            self.filtered_tasks = [task for task in self.filtered_tasks if task.completed]
        
        self.update_task_list()
    
    def clear_filters(self) -> None:
        """Clear all filters."""
        self.course_filter_var.set("All")
        self.priority_filter_var.set("All")
        self.status_filter_var.set("Pending")
        self.filtered_tasks = [task for task in self.current_tasks if not task.completed]
        self.update_task_list()
    
    def on_task_double_click(self, event) -> None:
        """Handle double-click on a task."""
        selection = self.task_tree.selection()
        if selection:
            task_id = int(selection[0])
            self.show_task_details(task_id)
    
    def show_task_details(self, task_id: int) -> None:
        """Show details for the selected task."""
        task = self.db.get_task(task_id)
        if not task:
            return
        
        # Enable buttons
        self.edit_btn.config(state=tk.NORMAL)
        self.delete_btn.config(state=tk.NORMAL)
        self.complete_btn.config(state=tk.NORMAL)
        self.complete_btn.config(
            text="Mark Incomplete" if task.completed else "Mark Complete"
        )
        
        # Display task details
        self.detail_text.delete(1.0, tk.END)
        details = f"""Title: {task.title}
Course: {task.course}
Priority: {task.priority.capitalize()}
Due Date: {task.due_date}
Countdown: {format_countdown(task.due_date)}

Description:
{task.description}

Created: {task.created_at}
Reminder: {task.reminder_time or 'None'}
Status: {'Completed' if task.completed else 'Pending'}"""
        
        self.detail_text.insert(1.0, details)
        self.current_task = task
    
    def show_add_task_dialog(self) -> None:
        """Show dialog to add a new task."""
        self.show_task_dialog()
    
    def show_edit_task_dialog(self) -> None:
        """Show dialog to edit the selected task."""
        if hasattr(self, 'current_task'):
            self.show_task_dialog(self.current_task)
    
    def show_task_dialog(self, task: Optional[Task] = None) -> None:
        """Show dialog to add or edit a task."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task" if task else "Add Task")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Variables
        title_var = tk.StringVar(value=task.title if task else "")
        description_var = tk.StringVar(value=task.description if task else "")
        course_var = tk.StringVar(value=task.course if task else "")
        priority_var = tk.StringVar(value=task.priority.capitalize() if task else "Medium")
        date_var = tk.StringVar(value="")
        time_var = tk.StringVar(value="23:59")
        reminder_var = tk.StringVar(value="")
        
        # Pre-populate date and time if editing
        if task and task.due_date:
            try:
                due_dt = datetime.fromisoformat(task.due_date)
                date_var.set(due_dt.strftime("%Y-%m-%d"))
                time_var.set(due_dt.strftime("%H:%M"))
            except ValueError:
                pass
        
        if task and task.reminder_time:
            # Calculate offset for display
            try:
                due_dt = datetime.fromisoformat(task.due_date)
                reminder_dt = datetime.fromisoformat(task.reminder_time)
                diff = due_dt - reminder_dt
                
                if diff.days > 0:
                    reminder_var.set(f"{diff.days} days")
                elif diff.seconds >= 3600:
                    hours = diff.seconds // 3600
                    reminder_var.set(f"{hours} hours")
                elif diff.seconds >= 60:
                    minutes = diff.seconds // 60
                    reminder_var.set(f"{minutes} minutes")
            except ValueError:
                pass
        
        # Create form
        form_frame = ttk.Frame(dialog, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=2)
        title_entry = ttk.Entry(form_frame, textvariable=title_var, width=30)
        title_entry.grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=2)
        description_entry = tk.Text(form_frame, height=4, width=30)
        description_entry.grid(row=1, column=1, sticky=tk.EW, pady=2)
        if task:
            description_entry.insert("1.0", task.description)
        
        # Course
        ttk.Label(form_frame, text="Course:").grid(row=2, column=0, sticky=tk.W, pady=2)
        course_entry = ttk.Entry(form_frame, textvariable=course_var, width=30)
        course_entry.grid(row=2, column=1, sticky=tk.EW, pady=2)
        
        # Priority
        ttk.Label(form_frame, text="Priority:").grid(row=3, column=0, sticky=tk.W, pady=2)
        priority_combo = ttk.Combobox(
            form_frame,
            textvariable=priority_var,
            values=["Low", "Medium", "High"],
            state="readonly",
            width=27
        )
        priority_combo.grid(row=3, column=1, sticky=tk.EW, pady=2)
        
        # Due Date
        ttk.Label(form_frame, text="Due Date:").grid(row=4, column=0, sticky=tk.W, pady=2)
        date_frame = ttk.Frame(form_frame)
        date_frame.grid(row=4, column=1, sticky=tk.EW, pady=2)
        
        date_entry = ttk.Entry(date_frame, textvariable=date_var, width=15)
        date_entry.pack(side=tk.LEFT)
        
        date_button = ttk.Button(
            date_frame,
            text="Today",
            command=lambda: date_var.set(date.today().strftime("%Y-%m-%d"))
        )
        date_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Due Time
        ttk.Label(form_frame, text="Due Time:").grid(row=5, column=0, sticky=tk.W, pady=2)
        time_entry = ttk.Entry(form_frame, textvariable=time_var, width=30)
        time_entry.grid(row=5, column=1, sticky=tk.EW, pady=2)
        
        # Reminder
        ttk.Label(form_frame, text="Reminder:").grid(row=6, column=0, sticky=tk.W, pady=2)
        reminder_entry = ttk.Entry(form_frame, textvariable=reminder_var, width=30)
        reminder_entry.grid(row=6, column=1, sticky=tk.EW, pady=2)
        ttk.Label(form_frame, text="(e.g., '48 hours', '30 minutes')").grid(
            row=7, column=1, sticky=tk.W, pady=0
        )
        
        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def save_task():
            # Validate input
            title = title_var.get().strip()
            if not title:
                messagebox.showerror("Error", "Title is required")
                return
            
            due_date_str = parse_datetime(date_var.get(), time_var.get())
            if not due_date_str:
                messagebox.showerror("Error", "Invalid date or time format")
                return
            
            # Calculate reminder time
            reminder_offset = reminder_var.get().strip()
            reminder_time = None
            if reminder_offset:
                reminder_time = calculate_reminder_time(due_date_str, reminder_offset)
                if not reminder_time:
                    messagebox.showerror("Error", "Invalid reminder format")
                    return
            
            # Create or update task
            if task:
                # Update existing task
                task.title = title
                task.description = description_entry.get("1.0", tk.END).strip()
                task.course = course_var.get().strip()
                task.priority = priority_var.get().lower()
                task.due_date = due_date_str
                task.reminder_time = reminder_time
                self.db.update_task(task)
                
                # Update notification if needed
                if reminder_time:
                    self.notification_manager.schedule_notification(
                        task.id,
                        reminder_time,
                        f"Reminder: {task.title}",
                        f"Task due: {task.due_date}"
                    )
                else:
                    self.notification_manager.cancel_scheduled_notification(task.id)
            else:
                # Create new task
                new_task = Task(
                    title=title,
                    description=description_entry.get("1.0", tk.END).strip(),
                    course=course_var.get().strip(),
                    priority=priority_var.get().lower(),
                    due_date=due_date_str,
                    reminder_time=reminder_time,
                    created_at=datetime.now().isoformat()
                )
                task_id = self.db.add_task(new_task)
                new_task.id = task_id
                
                # Schedule notification if needed
                if reminder_time:
                    self.notification_manager.schedule_notification(
                        task_id,
                        reminder_time,
                        f"Reminder: {new_task.title}",
                        f"Task due: {new_task.due_date}"
                    )
            
            # Refresh task list
            self.load_tasks()
            self.apply_filters()
            dialog.destroy()
        
        save_btn = ttk.Button(button_frame, text="Save", command=save_task)
        save_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT)
        
        # Focus on title entry
        title_entry.focus()
    
    def delete_selected_task(self) -> None:
        """Delete the selected task."""
        if not hasattr(self, 'current_task'):
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            self.db.delete_task(self.current_task.id)
            self.notification_manager.cancel_scheduled_notification(self.current_task.id)
            self.load_tasks()
            self.apply_filters()
            self.detail_text.delete(1.0, tk.END)
            self.edit_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)
            self.complete_btn.config(state=tk.DISABLED)
    
    def complete_selected_task(self) -> None:
        """Mark the selected task as complete or incomplete."""
        if not hasattr(self, 'current_task'):
            return
        
        self.current_task.completed = not self.current_task.completed
        self.db.update_task(self.current_task)
        
        if self.current_task.completed:
            # Cancel any scheduled notifications
            self.notification_manager.cancel_scheduled_notification(self.current_task.id)
        
        self.load_tasks()
        self.apply_filters()
        self.show_task_details(self.current_task.id)
    
    def export_tasks(self) -> None:
        """Export tasks to JSON file."""
        filename = f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=filename,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                self.db.export_tasks(filepath)
                messagebox.showinfo("Success", f"Tasks exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export tasks: {e}")
    
    def import_tasks(self) -> None:
        """Import tasks from JSON file."""
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                self.db.import_tasks(filepath)
                self.load_tasks()
                self.apply_filters()
                messagebox.showinfo("Success", "Tasks imported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import tasks: {e}")
    
    def show_calendar_view(self) -> None:
        """Show calendar view of tasks."""
        messagebox.showinfo("Calendar View", "Calendar view feature would be implemented here.")
    
    def show_settings(self) -> None:
        """Show settings dialog."""
        messagebox.showinfo("Settings", "Settings feature would be implemented here.")
    
    def toggle_dark_mode(self) -> None:
        """Toggle dark mode."""
        self.dark_mode = self.dark_mode_var.get()
        # In a full implementation, this would change the UI theme
        messagebox.showinfo("Dark Mode", "Dark mode toggle would be implemented here.")
    
    def on_closing(self) -> None:
        """Handle application closing."""
        self.notification_manager.stop_notification_service()
        self.root.destroy()


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = AcademicDeadlineTrackerUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()