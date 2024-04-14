## Notes on downloading (windows only)
prerequisite:
python scheduler:
 $ pip install schedule

Cloning the repo and running main.py should work fine so long as scheduler is installed.


## Inspiration
I took inspiration from the prompt "Social Good" to develop an application designed to help people with mental illnesses, ranging from memory loss to depression and anxiety. A journaling app that says kind words after you finish an entry seems like a great benefit to those people.

## What it does
At its core, it stores journal entries. After my experience trying (and failing) to use obsidian, notion, and several other applications to journal with, I decided that the best design for a journaling app is simplicity. With one keystroke, you can be on your way typing. It automatically sets up windows reminders with async as long as the app is open. It prompts the user to automatically add it to the windows startup registry, so it's always waiting on the desktop and can consistently deliver notifications. Even if it shuts down, it saves all userdata and journal entries in human-readable format, so people can customize as they wish even without the application. Finally, it gives randomized words of celebration/encouragement based on how a person rates their day versus their average rating.

## How I built it
It is built entirely in python, with minimal libraries to interact with windows.

## Challenges I ran into
Windows API is a nightmare to navigate. Finding a backwards-compatible (at least to both windows 10 and 11) solution to notifications was frustratingly complex. 

## Accomplishments that we're proud of
The additional features that take a little more know-how than just any journal, including windows notifications and startup

## What's next for iUnderstand
To continue the project, I plan to add a more robust list of computer-responses to days (100 of each kind might not be enough), add a way to track trends of day ratings other than reading your own entries, and add a measurement on how certain words appear in your entries versus how you rate a day. 
