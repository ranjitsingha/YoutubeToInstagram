import re
import requests
import random
import os
from datetime import datetime
from instagrapi import Client
import time
import subprocess
import urllib.parse
from local_lib.pytube.__main__ import YouTube as huggywuggywilleatyoucuzyouverytasty
    
def take_username_password_input():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    return username, password        

def get_short_videos(channel_link, num_videos=30):
    try:
        response = requests.get(channel_link)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return []

    video_links = re.findall(r'"/shorts/([^"]+)"', response.text)
    short_videos = ['https://www.youtube.com/shorts/' + link for link in video_links]
    return short_videos[:num_videos]
    
def downloadyoutubeshorts(video_url):
    try:
        yt = huggywuggywilleatyoucuzyouverytasty(video_url)
        stream = yt.streams.get_highest_resolution()
        if stream:
            video_title = stream.title
            print(f"Downloading ... {video_url}")
            path = stream.download()
            return path            
        else:
            return None
    except Exception as e:
        return None 
    
def uploadtoinstagram(videopath):
    print("Uploading to Instagram")  
    caption = "Interesting Facts 🤯 #trendingnow #trendingaudio #trendingnews #instagood #viral #gk #sciencefact #tech #techfact"     
    upload = cl.clip_upload(
        videopath,
        caption=caption, 
        location=None
    )    
    print("Video upload successful")
    save_to_file(uploaded_links_file, random_short_video)
    print("Saved link to uploadedlinks list")
    os.remove(videopath)
    print("Sleeping")   
    
def save_to_file(filename, data):
    with open(filename, 'a') as file:
        file.write(data + '\n')

def read_from_file(filename):
    if not os.path.exists(filename):
        open(filename, 'w').close()
        return []

    with open(filename, 'r') as file:
        return file.read().splitlines()                                      

def start():    
    channel_links = [
        "https://youtube.com/@shortsmine99?si=D1hZF6-SkiKF6TZB",
        "https://youtube.com/@factbeast90?si=BO_mX7_mkWVxfARy",
        "https://youtube.com/@the_fact?si=PECJUh3vttGA9qhn"
    ]    
    random_channel_link = random.choice(channel_links)
    print(f"Selected channel link: {random_channel_link}\n")
    short_videos = get_short_videos(random_channel_link)
    if short_videos:
        random_short_video = random.choice(short_videos)
        print(f"Selected short video link: {random_short_video}")
        if random_short_video not in read_from_file(uploaded_links_file):           
            try:
                videopath = downloadyoutubeshorts(random_short_video)
                if videopath is not None:
                    print(videopath)
                    uploadtoinstagram(videopath)
                else:
                    print("video download unsuccessful")    
                    start()
            except Exception as e:
                print(f"failed {str(e)}")
                start()
        else:
            start()    
    else:
        print("No short videos found.")
        start()

uploaded_links_file = 'uploadedlinks.txt'            
USERNAME, PASSWORD = take_username_password_input()
session_file = 'session.json'

if os.path.exists(session_file):
    print("Logging in to Instagram from previous session")
    cl = Client()
    cl.load_settings("session.json")
    cl.login (USERNAME, PASSWORD)
else:
    print("Logging in to Instagram")
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(session_file)        
    
while True:
    start()
    time.sleep(2 * 60 * 60)      
    
    
