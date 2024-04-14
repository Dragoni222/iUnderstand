from datetime import datetime
from os.path import exists
from JournalEntry import JournalEntry
import asyncio


class userdata:
    def __init__(self):
        self.num_of_entries = len(self.GetJournals())
        if not exists("UserData.txt"):
            data = open("UserData.txt", "w")
            data.write(
                "Startup: False\nMuteStartup: False\nNotifications: False\nMuteNotifications: False\nNotificationTime: "
                "20:00\nNotificationTitle: Reminder to write reflection\nNotificationMessage:"
                " hiiii this is your daily reminder to write a reflection of the day on iUnderstand :)")
            data.close()

    def SetSetting(self, setting, value):
        data = open("UserData.txt", "r")
        prevData = data.read()

        prevData = prevData.split("\n")
        data.close()
        dataFile = open("UserData.txt", "r")
        data = dataFile.readlines()
        dataFile.close()
        line = 0

        found = False
        while not found:
            currentLine = data[line]
            if currentLine.startswith(setting):
                found = True
            else:
                line += 1

        prevData.pop(line)
        prevData2 = prevData[(line):]
        prevData = prevData[:(line)]

        prevData2 = "\n".join(prevData2)
        prevData2 += "\n"
        prevData = "\n".join(prevData)
        if line != 0:
            prevData += "\n"
        data = open("UserData.txt", "w")

        data.writelines(prevData)
        data.write(setting + ": " + str(value) + "\n")
        data.writelines(prevData2)
        data.close()

    def GetSetting(self, setting, type):
        dataFile = open("UserData.txt", "r")
        data = dataFile.readlines()
        found = False
        line = 0
        while not found:
            currentLine = data[line]
            if currentLine.startswith(setting):
                return type(currentLine[len(setting) + 2:].strip())

            else:
                line += 1
        dataFile.close()

    def AddJournal(self, date, rating, notes):
        self.num_of_entries += 1
        journal = JournalEntry(date, rating, notes, self.num_of_entries)
        previousDataFile = open("UserData.txt", "r")
        previousData = previousDataFile.read()
        previousDataFile.close()
        data = open("UserData.txt", "w")
        data.write(previousData)
        data.write("\nBegin\n")
        data.write(str(journal.id) + "\n" + str(journal.date) + "\n" + str(journal.rating) + "\n" + journal.notes)
        data.write("\nEnd\n")
        data.close()

    def GetJournals(self):
        data = open("UserData.txt", "r")
        jid = False
        date = False
        rating = False
        body = False
        journals = []
        journal = []

        for line in data:

            if line.startswith("Begin"):
                jid = True
            elif jid:
                journal.append(int(line.strip()))
                date = True
                jid = False
            elif date:
                dateData = line.strip().split("-")
                timesplit = dateData[2].split(" ")
                dateData[2] = timesplit[0]
                dateData.append(timesplit[1])
                timeData = dateData[3].split(":")
                timeData[2] = timeData[2].split(".")[0]
                journal.append(
                    datetime(int(dateData[0]), int(dateData[1]), int(dateData[2]), int(timeData[0]), int(timeData[1])))

                date = False
                rating = True
            elif rating:
                journal.append(float(line.strip()))
                journal.append("")
                rating = False
                body = True
            elif body:
                if line.startswith("End"):
                    journal = JournalEntry(journal[1], journal[2], journal[3], journal[0])
                    journals.append(journal)
                    journal = []
                    body = False
                else:
                    journal[3] += line

        data.close()
        return journals

    #def GetJournal(self, id):

    def AverageRating(self):
        journals = self.GetJournals()
        total = 0
        for journal in journals:
            total += journal.rating

        return total / len(journals)
