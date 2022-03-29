# Importing all necessary modules/classes
from HabitTracker import HabitTracker


class Analytics(HabitTracker):
    """
    Analytics class for habit analysis created from parent class HabitTracker
    """

    def __init__(self):
        # Initiating super init class and inheriting parent class HabitTracker
        super().__init__()
        pass

    def amount_of_habits(self):
        """

        Returns: Number of currenlty tracked habits

        """
        amount = self.df.Description.count()
        print(f"The number of habits you are tracking: {amount}")

    def max_key(self):
        """
        :return: Habit with current longest streak
        """
        if len(self.data) == 0:
            # Max values from sample given that there are 0 entries in JSON file
            max_current_days = 194
            max_current_weeks = 27
            print(f"The longest current habit is \"Therapy\" with {max_current_days} days or "
                  f"{max_current_weeks} weeks!")
        else:
            # Max values from actual user data when there is at least one entry in JSON file
            max_current_days = 0
            max_current_weeks = 0
            key_current = "key"
            for key in self.data:
                max_new_days = self.data[key]["Streak (days)"]
                if max_new_days > max_current_days:
                    max_current_days = max_new_days
                    key_current = key
                max_new_weeks = self.data[key]["Streak (weeks)"]
                if max_new_weeks > max_current_weeks:
                    max_current_weeks = max_new_weeks
            print(f"The longest current habit is \"{key_current}\" with {max_current_days} days or "
                  f"{max_current_weeks} weeks!")
            # In case the user wants to use the Analytics function, the functionality is not impaired.
            # checking if there are any entries in the JSON file.
            # this typeof check allows the user to have habits with 0 counts and properly displayed 'Records column'.

    def total_days(self):
        """

        Returns: Total days of all habits tracked

        """
        total_days = self.df["Streak (days)"].sum()
        print(f"The total amount of days you are tracking is: {total_days}")

    def total_weeks(self):
        """

        Returns: Total days of all habits tracked

        """
        total_weeks = self.df["Streak (weeks)"].sum()
        print(f"The total amount of weeks you are tracking is: {total_weeks}")
        print("\n")