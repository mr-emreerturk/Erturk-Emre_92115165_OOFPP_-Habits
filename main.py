from Analytics import Analytics
from HabitTracker import HabitTracker
import os

# Create flag is_on for while loop
is_on = True
# Assign class to object
habit = HabitTracker()

# Start while loop. As long as is_on is True, while loop will continue.
while is_on:
    try:
        habit.update()
    except KeyError:
        # if the user deletes all entries and closes the app the file needs to be deleted as well because lined up JSON
        # are invalid when trying to read. It is better to create new 'habits.json from scratch as soon as the program
        # restarts.
        os.remove('habits.json')
        print("You have removed all entries from your tracker. Please restart the app.")
    # Print DataFrame
    habit.print_tracker()
    first_question = input("\nDo you want to 'edit', 'manage', 'analyze' habits or 'stop' the program? ").lower()
    if first_question == "edit":
        # Create flag for 'edit' answer
        edit_is_on = True
        # while 'edit' flag is True the question will repeat
        while edit_is_on:
            add_or_delete = input("Do you want to add, delete, or edit an existing habit? \n"
                                  "[Type 'back' to go back] ").lower()
            if add_or_delete == "add" or add_or_delete == "edit":
                # Both adding a new habit and editing an existing habit goes through the same process.
                # Create 'add' flag
                add_is_on = True
                # while 'add' flag is True the question will repeat
                while add_is_on:
                    # collect params by using input function
                    habit_name_add = input("Define the habit name: ").lower()
                    description = input("Describe your habit in 5 words: ")
                    daily_weekly = input("Do you want to track daily or weekly? ").lower()
                    start_date = input("When have you started? [YYYY-MM-DD] ")
                    # fill out params in add_entry method from HabitTracker class
                    habit.add_entry(habit_name_add, description, daily_weekly, start_date)
                    add_question = input("Do you want to add more habits? yes/no ").lower()
                    if add_question == "yes":
                        continue
                    else:
                        # Break while loop for 'add'
                        add_is_on = False
            elif add_or_delete == "delete":
                # Create 'delete' flag
                delete_is_on = True
                # while 'delete' flag is True the question will repeat
                while delete_is_on:
                    try:
                        habit_name_del = input("What's the habit? ").lower()
                        habit.delete_entry(habit_name_del)
                    except KeyError:
                        # If habit is not found user gets a notification.
                        print("I can't find this habit. Are you sure that you spelled it correctly?")
                        print("\n")
                    delete_question = input("Do you want to delete more habits? yes/no ").lower()
                    if delete_question == "no":
                        # Break while loop for 'delete'
                        delete_is_on = False
            else:
                # Break while loop for 'edit'
                edit_is_on = False
    elif first_question == "manage":
        try:
            broken_habit = input("Have you broken a habit? yes/no ").lower()
            if broken_habit == "no":
                pass
            elif broken_habit == "yes":
                which_habit_broken = input("Which habit have you broken? ").lower()
                habit.manage_habits(which_habit_broken)
                print(f"The habit '{which_habit_broken}' has been restarted, starting today.")
            else:
                print("Please answer with yes or no.")
        except KeyError:
            # Manage function can only be used if user input their own habits
            print("This is a sample table, please add your habits before accessing \'manage\' function. ")
    elif first_question == "analyze":
        # Initialize Analytics child-class an assign to object
        analytics = Analytics()
        analytics.amount_of_habits()
        analytics.max_key()
        analytics.total_days()
        analytics.total_weeks()

    elif first_question == "stop":
        # Stop app from running by turning flag as False
        is_on = False
    else:
        # Reminding user to stick to keywords
        print("Please answer with: \"edit\", \"manage\", \"analyze\", or \"stop\".")
        print("\n")