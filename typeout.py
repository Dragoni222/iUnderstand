import time


def typeout(string, wait):
    for letter in string:
        print(letter, end="")
        time.sleep(wait)
    
    
    