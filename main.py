from datetime import datetime

import balloontip
import windowsstartup
import pyuac
import schedule
import time

from JournalEntry import JournalEntry
from userdata import userdata


def main():
    data = userdata()
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
            if input("Set time for notifications? (default 20:00) (y/n) ").lower() == "y":
                correctFormat = False
                timeInput = ""
                while not correctFormat:
                    timeInput = input("Enter time: (HH:MM, 24hr): ")
                    correctFormat = validate_time_format(timeInput)
                data.SetSetting("NotificationTime", timeInput)

            data.SetSetting("Notifications", True)
            data.SetSetting("MuteNotifications", True)
        elif input("Don't ask again? (y/n) ").lower() == "y":
            data.SetSetting("MuteNotifications", True)

    if data.GetSetting("Notifications", str2bool):
        schedule.every().day.at(data.GetSetting("NotificationTime", str)).do(balloontip.balloon_tip(
            data.GetSetting("NotificationTitle", str), data.GetSetting("NotificationMessage", str)))

    while True:
        schedule.run_pending()
        time.sleep(1)


def str2bool(v):
    return v.lower() in ("true")


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
    main()
