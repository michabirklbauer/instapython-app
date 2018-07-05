#!/usr/bin/env python3

import platform
import os

if __name__ == '__main__':

    channel = input("Enter a Telegram channel in the form of ID (number) or @channelname:\n")
    api_token = input("Enter a Telegram bot API token:\n")
    rtime = input("Enter how long the bot should run in seconds (0 if bot should run infinitely):\n")
    stime = input("Enter the hour when story notifications should be sent:\n")
    debugging_mode = input("Enter if debugging mode should be activated: true/false\n")
    user_ids = []
    while True:
        user_id = input("Enter a user ID:\n")
        user_ids.append(user_id)
        confirm = input("Do you want to add another user ID? Yes/No\n")
        if str(confirm) in ["no", "No", "NO", "n", "0"]:
            break
    script = "bin/python/requesthandler.py instabot"
    user_ids_string_raw = ""
    for user_id in user_ids:
        user_ids_string_raw = user_ids_string_raw + str(user_id) + ";"
    user_ids_string = user_ids_string_raw.rstrip(";")
    if "Windows" in platform.system():
        cmd = "python " + script + " " + channel + " " + api_token + " " + rtime + " " + stime + " " + debugging_mode + " " + user_ids_string
        os.system(cmd)
    else:
        cmd = "python3 " + script + " " + channel + " " + api_token + " " + rtime + " " + stime + " " + debugging_mode + " " + user_ids_string
        os.system(cmd)
