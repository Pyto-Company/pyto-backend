from datetime import datetime


class NotificationService():

    def should_generate_notification(
        creation_date: str, interval_days: int, reminder_time: str
    ) -> bool:
        """
        Determine if a notification should be generated today.

        Args:
            creation_date (str): Date the reminder was created (format: 'YYYY-MM-DD').
            interval_days (int): Interval in days between reminders.
            reminder_time (str): Time of the reminder (format: 'HH:MM').

        Returns:
            bool: True if notification should be generated today, False otherwise.
        """
        # Parse inputs
        creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
        reminder_time = datetime.strptime(reminder_time, "%H:%M").time()
        today = datetime.now()
        
        # Calculate the difference in days
        delta_days = (today.date() - creation_date.date()).days

        # Check if the day is valid (delta_days must be a non-negative multiple of interval_days)
        if delta_days >= 0 and delta_days % interval_days == 0:
            # Check if the current time has reached or passed the reminder time
            if today.time() >= reminder_time:
                return True
        
        return False