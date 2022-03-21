# Importing all necessary  modules/classes
from datetime import date
import pandas as pd
import json
from tabulate import tabulate


# Creating HabitTracker Class
class HabitTracker:
    """
    PARENT CLASS EXECUTING THE BACKBONE OF HABIT TRACKER APP
    _______________________________________________________

    Methods:
        print_tracker: Prints habit tracker DataFrame
        add_entry: Adds entry to dictionary and saves new DICT in JSON file 'habits.json'
        delete_entry: Deletes entry from JSON file 'habits.json' and eliminates it from DataFrame
        manage_habits: Let's user manage habits if habits were broken today
        update: refreshes the app so that all calculations for streaks and records are up to date
    """

    def __init__(self):
        """
            PARENT CLASS EXECUTING THE BACKBONE OF HABIT TRACKER APP
            _______________________________________________________

            Methods:
                print_tracker: Prints habit tracker DataFrame
                add_entry: Adds entry to dictionary and saves new DICT in JSON file 'habits.json'
                delete_entry: Deletes entry from JSON file 'habits.json' and eliminates it from DataFrame
                manage_habits: Let's user manage habits if habits were broken today
                update: refreshes the app so that all calculations for streaks and records are up to date
            """
        try:
            # Opens existing file by opening context manager through 'with' statement
            with open("habits.json", "r") as json_file:
                data = json.load(json_file)
                self.data = data
                self.df = pd.DataFrame.from_dict(self.data, orient="index")
                self.df.sort_values(by="Streak (days)", ascending=True, inplace=True)
        except (ValueError, FileNotFoundError):
            # Creates sample habit tracker Data Frame if the app launches for first time and therefore avoids
            # 'ValueError' and 'FileNotFoundError'
            print("This is a sample habit tracker for you to understand the app better. ")
            self.data = {"Workout":
                             {"Description": "Sweat for 20 min",
                              "Daily/Weekly": "daily",
                              "Date started": "2022-02-01",
                              "Streak (days)": 41,
                              "Streak (weeks)": 5,
                              "Record": 41,
                              },
                         "Code":
                             {"Description": "Get better at Python",
                              "Daily/Weekly": "daily",
                              "Date started": "2022-02-01",
                              "Streak (days)": 41,
                              "Streak (weeks)": 5,
                              "Record": 53,
                              },
                         "Drink":
                             {"Description": "min. 3l",
                              "Daily/Weekly": "daily",
                              "Date started": "2022-01-01",
                              "Streak (days)": 72,
                              "Streak (weeks)": 10,
                              "Record": 72,
                              },
                         "Therapy":
                             {"Description": "Go to Therapy regularly",
                              "Daily/Weekly": "weekly",
                              "Date started": "2021-09-01",
                              "Streak (days)": 194,
                              "Streak (weeks)": 27,
                              "Record": 191,
                              },
                         "Sleep":
                             {"Description": "Sleep 7-9hrs per night",
                              "Daily/Weekly": "daily",
                              "Date started": "2022-03-01",
                              "Streak (days)": 13,
                              "Streak (weeks)": 1,
                              "Record": 35,
                              },
                         }

            for habit in self.data:
                # This for loop loops through all currently saved habits and refreshes today's date, so that all days
                # and weeks are correctly displayed
                x = self.data[habit]["Date started"]
                d1 = date(int(x[:4]), int(x[5:7]), int(x[8:]))
                today = date(int(date.today().strftime("%Y")), int(date.today().strftime("%m")),
                             int(date.today().strftime("%d")))
                # for days
                delta = today - d1
                delta_days = delta.days
                self.data[habit]["Streak (days)"] = delta_days
                # for weeks
                delta_weeks = today - d1
                delta_weeks = delta_weeks.days
                delta_weeks = int(int(delta_weeks) / 7)
                self.data[habit]["Streak (weeks)"] = delta_weeks
                # for records (for simplicity: +12)
                self.data[habit]["Record"] = delta_days + 12

            self.df = pd.DataFrame.from_dict(self.data, orient="index")
            self.df.sort_values("Streak (days)", inplace=True)

            # Delete sample entries so that user doesn't have to delete themselves
            del self.data["Workout"]
            del self.data["Code"]
            del self.data["Drink"]
            del self.data["Therapy"]
            del self.data["Sleep"]

    def print_tracker(self):
        """
        Prints habit tracker DataFrame

        Returns: DataFrame

        """
        print(tabulate(self.df, tablefmt="fancy_grid", headers="keys"))

    def add_entry(self, habit_name: object, description: object, daily_weekly: object, date_started: object):
        """
        adds entries to the dataframe and saves the entries in JSON file 'habits.json'.

        :param habit_name: name of the habit to be added
        :param description: short description of the habit to be added
        :param daily_weekly: daily or weekly tracking of the habit
        :param date_started: start of habit tracking
        :return: adding to dictionary which gets stored in json file
        """

        def calculate_current_streak_days():
            """
            Calculates current streak in days.

            :return: Current streak in days
            """
            # Extract started date as string
            x = self.data[habit_name]["Date started"]
            # Transform 'Date started' to datetime format
            d1 = date(int(x[:4]), int(x[5:7]), int(x[8:]))
            # Get today's date
            today = date(int(date.today().strftime("%Y")), int(date.today().strftime("%m")),
                         int(date.today().strftime("%d")))
            # Compute timedelta in days as integer
            delta = today - d1
            delta = delta.days
            return int(delta)

        def calculate_current_streak_weeks():
            """
            Calculates current streak in days.

            :return: Current streak in weeks
            """
            # Extract started date as string
            x = self.data[habit_name]["Date started"]
            # Transform 'Date started' to datetime format
            d1 = date(int(x[:4]), int(x[5:7]), int(x[8:]))
            # Get today's date
            today = date(int(date.today().strftime("%Y")), int(date.today().strftime("%m")),
                         int(date.today().strftime("%d")))
            # Compute timedelta in weeks as integer
            delta = today - d1
            delta = delta.days
            return int(int(delta) / 7)

            # if int(self.data[habit_name]["Streak (days)"]) > int(self.data[habit_name]["Highscore"]):
            #     self.data[habit_name]["Highscore"] = self.data[habit_name]["Streak (days)"]

        # Mock dataframe for new habit to make functions 'calculate_current_streak_days' and
        # 'calculate_current_streak_weeks' work
        self.data[habit_name] = {
            "Description": description,
            "Daily/Weekly": daily_weekly,
            "Date started": date_started,
            "Streak (days)": 0,
            "Streak (weeks)": 0,
            "Record": 0,
        }
        # updated dictionary including the correct number of days
        self.data[habit_name] = {
            "Description": description,
            "Daily/Weekly": daily_weekly,
            "Date started": date_started,
            "Streak (days)": calculate_current_streak_days(),
            "Streak (weeks)": calculate_current_streak_weeks(),
            "Record": calculate_current_streak_days(),
        }

        # save in json
        with open("habits.json", "w") as f:
            json.dump(self.data, f, indent=2)
        # reassign updated dictionary to DataFrame
        self.df = pd.DataFrame.from_dict(self.data, orient="index")
        print(f"\n")

    def delete_entry(self, habit_name):
        """
        Deletes entry from JSON file 'habits.json' and eliminates it from DataFrame

        :param habit_name: the name of the habit that needs to be deleted

        :return: deletes habit from habit tracker data frame
        """

        # Pops habit to be deleted from dictionary
        self.data.pop(habit_name)
        # reassign updated dictionary to DataFrame
        self.df = pd.DataFrame.from_dict(self.data, orient="index")
        print(f"\n")
        # Saves in updated dictionary in JSON file
        with open("habits.json", "w") as f:
            json.dump(self.data, f, indent=2)

    def manage_habits(self, broken_habit_name):
        """
        Manages habits by inserting habit key. Then drills into nested dictionary to reset 'Date started' to today's date.

        :param broken_habit_name: habit name that needs to be managed

        :return: updates user if habit was broken or not
        """

        def calculate_current_streak_days():
            """
            Calculates current streak in days.

            :return: Current streak in days
            """
            # Extract started date as string
            x = self.data[broken_habit_name]["Date started"]
            # Transform 'Date started' to datetime format
            d1 = date(int(x[:4]), int(x[5:7]), int(x[8:]))
            # Get today's date
            today_date = date(int(date.today().strftime("%Y")), int(date.today().strftime("%m")),
                              int(date.today().strftime("%d")))
            # Compute timedelta in days as integer
            delta = today_date - d1
            delta = delta.days
            return int(delta)

        def calculate_current_streak_weeks():
            """
            Calculates current streak in days.

            :return: Current streak in weeks
            """
            # Extract started date as string
            x = self.data[broken_habit_name]["Date started"]
            # Transform 'Date started' to datetime format
            d1 = date(int(x[:4]), int(x[5:7]), int(x[8:]))
            # Get today's date
            today_date = date(int(date.today().strftime("%Y")), int(date.today().strftime("%m")),
                              int(date.today().strftime("%d")))
            # Compute timedelta in weeks as integer
            delta = today_date - d1
            delta = delta.days
            return int(int(delta) / 7)

        # Get today's date
        today = date(int(date.today().strftime("%Y")), int(date.today().strftime("%m")),
                     int(date.today().strftime("%d")))
        # Replace 'Date started' with todays date in nested dictionary
        self.data[broken_habit_name]["Date started"] = today.strftime("%Y-%m-%d")
        # Compute streak for days/weeks
        self.data[broken_habit_name]["Streak (days)"] = calculate_current_streak_days()
        self.data[broken_habit_name]["Streak (weeks)"] = calculate_current_streak_weeks()
        # reassign updated dictionary to DataFrame
        self.df = pd.DataFrame.from_dict(self.data, orient="index")
        # save in JSON
        with open("habits.json", "w") as f:
            json.dump(self.data, f, indent=2)
        # If the streak of the newly ended habit is bigger than the Record than replace old record with new record
        # reassign updated dictionary to DataFrame
        if self.data[broken_habit_name]["Streak (days)"] > self.data[broken_habit_name]["Records"]:
            self.data[broken_habit_name]["Records"] = self.data[broken_habit_name]["Streak (days)"]
            with open("habits.json", "w") as f:
                json.dump(self.data, f, indent=2)
            self.df = pd.DataFrame.from_dict(self.data, orient="index")

    def update(self):
        """
        Refreshes the app so that all calculations for streaks and records are up to date.
        Uses for loop to loop through all currently saved habits.

            - updated dictionary and save in JSON File
            - sorted DataFrame, sorted by 'Streak (days)'

        :return: updated dictionary and save in JSON File, sorted DataFrame, sorted by 'Streak (days)'

        """

        for habit in self.data:
            # This for loop loops through all currently saved habits and refreshes today's date, so that all days
            # and weeks are correctly displayed
            x = self.data[habit]["Date started"]
            d1 = date(int(x[:4]), int(x[5:7]), int(x[8:]))
            today = date(int(date.today().strftime("%Y")), int(date.today().strftime("%m")),
                         int(date.today().strftime("%d")))
            # for days
            delta = today - d1
            delta_days = delta.days
            self.data[habit]["Streak (days)"] = delta_days
            # for weeks
            delta_weeks = today - d1
            delta_weeks = delta_weeks.days
            delta_weeks = int(int(delta_weeks) / 7)
            self.data[habit]["Streak (weeks)"] = delta_weeks

        # Sort updated DataFrame by 'Streak (days)'
        self.df.sort_values(by="Streak (days)", ascending=True, inplace=True)