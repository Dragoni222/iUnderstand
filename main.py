import asyncio
import random
from datetime import datetime
import balloontip
import typeout
import windowsstartup
import schedule
import time
from userdata import userdata


async def main():
    data = userdata()
    task1 = None
    if not data.GetSetting("Startup", str2bool) and not data.GetSetting("MuteStartup", str2bool):
        print(
            "I recommend that you set this application to run on startup so it can always notify you when to write your daily reflection.")
        if input("Set to run on startup? (y/n) ").lower() == "y":
            windowsstartup.add_to_startup()
            data.SetSetting("Startup", True)
            data.SetSetting("MuteStartup", True)
        elif input("Don't ask again? (y/n) ").lower() == "y":
            data.SetSetting("MuteStartup", True)

    if not data.GetSetting("Notifications", str2bool) and not data.GetSetting("MuteNotifications", str2bool):
        if input("Turn on notifications? (y/n) ").lower() == "y":
            data.SetSetting("Notifications", True)
            data.SetSetting("MuteNotifications", True)
            if input("Set time for notifications? (default 20:00) (y/n) ").lower() == "y":
                correctFormat = False
                timeInput = ""
                while not correctFormat:
                    timeInput = input("Enter time: (HH:MM, 24hr): ")
                    correctFormat = validate_time_format(timeInput)
                data.SetSetting("NotificationTime", timeInput)
            if input("Set custom message for notifications? (y/n) ").lower() == "y":
                data.SetSetting("NotificationTitle", input("Enter title of notification: "))
                data.SetSetting("NotificationMessage", input("Enter body of notification: "))

        elif input("Don't ask again? (y/n) ").lower() == "y":
            data.SetSetting("MuteNotifications", True)

    if data.GetSetting("Notifications", str2bool):
        schedule.every().day.at(data.GetSetting("NotificationTime", str)).do(balloontip.balloon_tip,
                                                                             data.GetSetting("NotificationTitle", str),
                                                                             data.GetSetting("NotificationMessage",
                                                                                             str))
        task1 = asyncio.create_task(checknotif())

    end = False
    while not end:
        print("1) Write journal entry")
        print("2) Read journal entries")
        print("3) Settings")
        print("4) Exit")

        userInput = input("Enter your choice: ")

        if userInput == "1":
            ratingFormat = False
            rating = 5
            while not ratingFormat:
                rating = input("Enter a numerical rating of today: ")
                try:
                    rating = float(rating)
                    ratingFormat = True
                except ValueError:
                    pass

            userInput = input("Notes about today (double-press enter to end):\n ")
            notes = ""
            while userInput != "":
                userInput += "\n"
                notes += userInput
                userInput = input()
            data.AddJournal(datetime.now(), rating, notes)
            print("Journal added.")
            if rating < (data.AverageRating() * 4) / 5:
                if input(
                        "It appears today was a below average day for you. Would you like some encouragement? (y/n): ").lower() == "y":
                    baddays = open("baddays", "r")
                    lines = baddays.readlines()
                    baddays.close()
                    typeout.typeout(random.choice(lines), 0.05)
                    input("Enter to continue...")

            elif rating > (data.AverageRating() * 6) / 5:
                if input(
                        "It appears today was an above average day for you. Would you like me to celebrate with you? (y/n): ").lower() == "y":
                    gooddays = open("gooddays", "r")
                    lines = gooddays.readlines()
                    gooddays.close()
                    typeout.typeout(random.choice(lines), 0.05)
                    input("Enter to continue...")
            else:
                input("Enter to continue...")



        elif userInput == "2":
            for entry in data.GetJournals():
                print()
                print(str(entry))
                print()
            input("Enter to continue...")
        elif userInput == "3":
            endSettings = False
            while not endSettings:
                print("1) Notifications")
                startup = data.GetSetting("Startup", str2bool)
                if not startup:
                    print("2) Launch on Startup")
                    print("3) Exit")
                else:
                    print("2) Exit")

                userInput = input("Enter your choice: ")

                if userInput == "1":
                    if data.GetSetting("Notifications", str2bool) or input(
                            "Turn on notifications? (y/n) ").lower() == "y":
                        data.SetSetting("Notifications", True)
                        data.SetSetting("MuteNotifications", True)
                    if input("Set time for notifications? (currently " + data.GetSetting("NotificationTime",
                                                                                         str) + ") (y/n) ").lower() == "y":
                        correctFormat = False
                        timeInput = ""
                        while not correctFormat:
                            timeInput = input("Enter time: (HH:MM, 24hr): ")
                            correctFormat = validate_time_format(timeInput)
                        data.SetSetting("NotificationTime", timeInput)
                    if input("Set custom message for notifications? (y/n) ").lower() == "y":
                        data.SetSetting("NotificationTitle", input("Enter title of notification: "))
                        data.SetSetting("NotificationMessage", input("Enter body of notification: "))
                    print("Notification settings will take effect next time you open the app.")
                    input("Enter to continue...")

                elif userInput == "2" and not startup:
                    if input("Launch on startup? (y/n) ").lower() == "y":
                        data.SetSetting("Startup", True)
                        data.SetSetting("MuteStartup", True)
                        windowsstartup.add_to_startup()
                elif userInput == "2" or userInput == "3":
                    endSettings = True




        elif userInput == "4":
            end = True
            if data.GetSetting("Notifications", str2bool):
                task1.cancel()


def str2bool(v):
    return v.lower() in "true"


async def checknotif():
    while True:
        schedule.run_pending()
        time.sleep(5)


def validate_time_format(time_str):
    # Split the string by ':' to separate hours and minutes
    time_components = time_str.split(':')

    # Check if there are two components (hours and minutes)
    if len(time_components) != 2:
        return False

    # Check if the hours and minutes are numeric
    if not time_components[0].isdigit() or not time_components[1].isdigit():
        return False

    # Extract hours and minutes
    hours = int(time_components[0])
    minutes = int(time_components[1])

    # Check if hours and minutes are within the valid range
    if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
        return False

    return True


if __name__ == '__main__':
    asyncio.run(main())
