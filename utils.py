# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 15:40:27 2019

@author: YGOBEI05
"""

import urllib
from bs4 import BeautifulSoup
from pytube import YouTube
import cv2
import os
import glob


def get_urls(text, limit=10):
    '''Search for a phrase on Youtube and returns a list of links to the first videos
        that are returned. A maximum of results can be set (default 10).'''
        
    query = urllib.parse.quote(text)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for i, vid in enumerate(soup.findAll(attrs={'class':'yt-uix-tile-link'})):
        if i < limit:
            urls.append('https://www.youtube.com' + vid['href'])
    print(f"Found {len(urls)} video links for {text}")
    return urls


def download_video(url, path=None, max_duration=10):
    '''Download Youtube video from the url to the path specified, or the cwd if non specified.
        Only videos shorter than max_duration are downloaded and reports are printed to say which
         video is downloaded successfully.'''
         
    try:
        yt = YouTube(url)
        duration = int(yt.player_config_args['player_response']['streamingData']['formats'][0]['approxDurationMs'])
        if duration < max_duration*60*1000:
            yt = yt.streams.filter(file_extension='mp4').first()
            out_file = yt.download(path)
            file_name = out_file.split("\\")[-1]
            print(f"Downloaded {file_name} correctly!")
        else:
            print(f"Video {url} too long")
    except Exception as exc:
        print(f"Download of {url} did not work because of {exc}...")
    
    
def max_label(name, folder):
    '''Look at a folder and check the files with pattern "name_###.jpg" to extract the
    largest label present.'''
    
    path_pattern = os.path.join(folder, name + "_*.jpg")
    existing_files = glob.glob(path_pattern)
    if not existing_files:
        biggest_label = 0
    else:
        existing_labels = map(lambda s: int(s.split('_')[-1].split('.')[0]), existing_files)
        biggest_label = max(existing_labels)
    return biggest_label
    
    
def extract_images_from_video(video, folder=None, delay=30, name="file", max_images=20, silent=False):
    '''Read a downloaded video from its path and extract screenshots every few seconds, set by the delay parameter.
        Images are saved in the specified folder or the cwd if none is specified and a maximum number of
        screenshots can be specified. The files are named "name_##.jpg" and the labelling starts where it already stops
        in the folder.'''
    
    vidcap = cv2.VideoCapture(video)
    count = 0
    num_images = 0
    if not folder:
        folder = os.getcwd()
    label = max_label(name, folder)
    success = True
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    
    while success and num_images < max_images:
        success, image = vidcap.read()
        num_images += 1
        label += 1
        file_name = name + "_" + str(label) + ".jpg"
        path = os.path.join(folder, file_name)
        cv2.imwrite(path, image)
        if cv2.imread(path) is None:
            os.remove(path)
        else:
            if not silent:
                print(f'Image successfully written at {path}')
        count += delay*fps
        vidcap.set(1, count)
        
        
def extract_images_from_word(text, delete_video=False, image_delay=30, 
                             num_urls=10, max_images=20, name="file", max_duration=15, silent=False):
    '''Search for a phrase on Youtube, download a specified number of videos from the results and extract 
        screenshots from them with a specified time delay between each. A folder is created in the cwd
         to store the images, which are named "name_###.jpg". If the folder already exists, the labelling
         starts where it stopped before. Videos are deleted after the extraction.'''
    
    if not os.path.exists(name):
        os.mkdir(name)
    urls = get_urls(text, num_urls)
    for url in urls:
        download_video(url, max_duration=max_duration)
    for i, video in enumerate(glob.glob("*.mp4")):
        extract_images_from_video(video, folder=name, delay=image_delay, name=name, max_images=max_images, silent=silent)
        if delete_video:
            os.remove(video)
            
