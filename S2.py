import os
import subprocess
import requests
from art import *

class S2:
    def __init__(self):
        self.data = []

    def formatfile(self, file):
        dict = {}  # Empty dictionary
        tmp = ""  # Empty array
        idx = 0

        # For loop that iterates through all the file
        for c in file:
            if c != '\n':
                tmp += c
            else:
                if tmp[0] == "[" and tmp[-1] == "]" and tmp[1] != "/":
                    var_name = tmp[1].upper() + tmp[2:-1].lower()
                    if var_name == "Stream":
                        dict[var_name + " " + str(idx)] = {}
                    else:
                        dict[var_name] = {}
                elif tmp[0] == "[" and tmp[-1] == "]" and tmp[1] == "/":
                    if var_name == "Stream":
                        idx += 1
                else:
                    i = tmp.find("=")
                    if var_name == "Stream":
                        dict[var_name + " " + str(idx)][tmp[:i]] = tmp[i + 1:]
                    else:
                        dict[var_name][tmp[:i]] = tmp[i + 1:]

                tmp = ""  # Empty array

        return dict  # Return dictionary

    def iscompatible(self, video, audio):
        broadcasting_standards = {
            "DVB": {
                "video": ["mpeg2", "h264"],
                "audio": ["aac", "ac3", "mp3"]
            },
            "ISDB": {
                "video": ["mpeg2", "h264"],
                "audio": ["aac"]
            },
            "ATSC": {
                "video": ["mpeg2", "h264"],
                "audio": ["ac3"]
            },
            "DTMB": {
                "video": ["mpeg2", "h264", "avs", "avs+"],
                "audio": ["aac", "ac3", "mp3", "mp2", "dra"]
            }
        }
        arr = []  # Array to return
        for b in broadcasting_standards:
            if video in broadcasting_standards[b]["video"] and audio in \
                    broadcasting_standards[b]["audio"]:
                arr.append(b)

        return arr

    def exercise1(self):
        subprocess.call("ffplay -flags2 +export_mvs -i bbb.mp4 -vf codecview=mv=pf+bf+bb",
                        shell=True)

    def exercise2(self):
        start = "00:00:00.0"
        ending = "00:01:00.0"

        subprocess.call(
            ['ffmpeg', '-ss', start, '-i', 'bbb.mp4', '-c', 'copy', '-t',
             ending, 'cut_bbb.mp4'])
        subprocess.call(
            ['ffmpeg', '-ss', start, '-i', 'bbb.mp4', '-vn', '-acodec', 'mp3',
             '-t', ending, 'bbb_mp3.mp3'])
        subprocess.call(
            ['ffmpeg', '-ss', start, '-i', 'bbb.mp4', '-vn', '-acodec', 'aac',
             '-aac_coder', 'twoloop', '-t', ending, 'bbb_aac.aac'])
        subprocess.call(
            "ffmpeg -i cut_bbb.mp4 -i bbb_aac.aac -i bbb_mp3.mp3 -map 0:v -map 0:a -map 1:a bbb_container.mp4",
            shell=True)

    def exercise3(self):
        subprocess.call(
            "ffprobe -i bbb_container.mp4 -show_format -show_streams > metadata.json",
            shell=True)  # Create JSON file with metadata
        f = open("metadata.json", 'r')  # Open JSON file
        dict = self.formatfile(f.read())  # Create dictionary from JSON file

        print("This MP4 container has...")
        video = []
        audio = []

        # Extract video and audio codecs from dictionary
        for stream in dict:
            if "codec_type" in list(dict[stream].keys()):
                if dict[stream]["codec_type"] == "video":
                    video.append(dict[stream]['codec_name'])
                    print("- A(n) " + dict[stream]['codec_name'] + " video.")
                elif dict[stream]["codec_type"] == "audio":
                    audio.append(dict[stream]['codec_name'])
                    print("- A(n) " + dict[stream]['codec_name'] + " audio.")

        print(
            "And the broadcasting standards compatible with these formats are...")
        counter = 0

        # Iterate through all video and audio formats
        for v in video:
            for a in audio:
                arr = self.iscompatible(v,
                                   a)  # Check if there is a compatible broadcasting standard
                if len(arr) > 0:
                    print(
                        "- With " + str(v) + " video and " + str(a) + " audio:",
                        arr)
                    counter += 1

        # If no broadcasting standard is detected, then show "none"
        if counter == 0:
            print("...none. I'm sorry :(")

        os.remove("metadata.json")  # Delete JSON file

    def exercise4(self):
        start = "00:00:00.0"
        ending = "00:01:00.0"

        path = "http://arnaublanco.github.io/subtitles.srt"
        response = requests.get(path)  # Download subtitles file
        with open("subtitles.srt", 'wb') as f:
            f.write(response.content)  # Extract content from file
        subprocess.call(['ffplay', '-i', 'bbb.mp4', '-ss', start, '-vf',
                         'subtitles=subtitles.srt', '-t', ending])

    def run(self):
        os.chdir('video')
        tprint("Welcome Javi!")
        print("Welcome to Lab 3 of the Audio and Video Encoding Systems.")

        while(1):
            print('------------------------------------------')
            print("Please select what exercise you'd like to run:")
            print("1. Exercise 1.")
            print("2. Exercise 2.")
            print("3. Exercise 3.")
            print("4. Exercise 4.")
            print("0. Exit.")
            option = input('Select your option here: ')
            if option != "0":
                print('------------------------------------------')
                print('EXERCISE ' + str(option))
                print('------------------------------------------')

            if option == "1":
                self.exercise1()
            elif option == "2":
                self.exercise2()
            elif option == "3":
                self.exercise3()

            elif option == "4":
                self.exercise4()

            elif option == "0":
                print('------------------------------------------')
                print("Thanks for you attention!")
                tprint("Bye Javi!")
                break
            else:
                print("The option you wrote is not valid!")