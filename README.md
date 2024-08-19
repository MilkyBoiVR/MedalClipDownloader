# MedalDownloader
An automation script thta downloads all your clips from Medal.TV while also allowing you to select specific visibility and game clips.
# Basic Installation
Head over to [Releases](https://github.com/MilkyBoiVR/MedalDownloader/releases) and download `MedalDownloader.zip`
# Developer Installation
1. Download latest version of [Python](https://www.python.org/downloads/) (Ensure Python is added to PATH)
2. Run `pip install customtkinter opencv-python pyautogui numpy pyperclip requests beautifulsoup4`
3. Download `button.png` `clicked.png` `MedalDownloader.py`
# Usage
A guide on how to use the tool without any issues
## 1. Library and Filters
Library is the best way to download the clips using their buttons through image recognition. Selecting wanted filters will allow you to select the clips you want based on Game, Visibility, Type, Hashtags, People.
![1-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/e1fb2eec-845c-49ea-a793-8ae8d0124a52)
## 2. Preload
Scroll down to the bottom of your medal clips, this helps preload the buttons to allow link copying.
![2-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/8ecf6e39-aef4-4155-a869-f6d5e54febfd)
## 3. Downloading (DO NOT MOVE MOUSE)
Select where you want the clips to be downloaded to using "Browse" and start the tool using "Start Download". 
> [!WARNING]
> 1. If the tool is above a "Copy Link" button, the tool will skip that specific clip.
>
> 2. If you move your mouse during "Copy Link" issues may occur.

![3-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/44e7c8ce-d7e0-480a-b2a4-1b3d425fcad2)
## 4. View downloaded clips
Click "View Videos" and all *currently* downloaded clips will be shown. 
![4-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/45200a58-58d3-417d-98a7-dac24e45e6c3)

# Information
- Mass downloads on Medal has been a wanted feature for a very long time. But with no actual evidence of such a feature being worked on by the Medal developers, I've decided to push out this tool for anyone to use.
- With the way the tool is structured, changes of the Medal.TV UI may cause the tool to break and cause issues, or simply not work at all. The only way to maintain this is through frequent updates. I do not have the time or effort to keep on updating this project.
- To keep this project alive, I will allow people to commit changes and I will personally review all requests made on this page.
- If there are any issues then contact @MilkyBoiVR on Discord.
