import os
import sys
import json
import random
import time
import sqlite3
import argparse
import traceback
import base64
import dataset
import requests

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pprint import pprint
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.exc import ProgrammingError
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Videos to images')
parser.add_argument('--hashtag', type=str, help='Hashtag name')
parser.add_argument('--output_dir', type=str, help='Output dir for hashtags data')
args = parser.parse_args()

hashtag_path = "https://www.instagram.com/explore/tags/" + args.hashtag + "/"

options = Options()
options.headless = False

profile = webdriver.FirefoxProfile()
profile.set_preference("media.volume_scale", "0.0")

driver = webdriver.Firefox(options=options, firefox_profile=profile)
actionChains = ActionChains(driver)

print("Getting the webpage")

driver.get(hashtag_path)
final_array = []
visited = {}
for i in range(50):
    a_name_array = (driver.find_elements_by_xpath("//a[@href]"))
    for ele in a_name_array:
        link = ele.get_attribute("href")
        if link not in visited and "/p/" in link:
            visited[link] = True
            print(link)
            final_array.append(link)
    actionChains.send_keys(Keys.END).perform()
    time.sleep(2)
driver.close()
driver.quit()

print(len(final_array))

headers = {
    'authority': 'www.instagram.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'dnt': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': 'mcd=3; mid=W6Y23QAEAAFCrQGU-Biy8KQormLH; fbm_124024574287414=base_domain=.instagram.com; csrftoken=EQp2v3VktI8Ukzl1Mdl3qIjw6gYSnVKl; ds_user_id=12609073606; sessionid=12609073606%3ANrq5UW3yZrmCuA%3A14; rur=FRC; urlgen="{\\"14.139.82.6\\": 55824}:1hFf7n:txypGvUAyCDpMJndpYSZ3GGqzdI"',
}

params = (
    ('__a', '1'),
)
comments={}
likes={}
video={}
text={}
json_data = {}
json_response_dict={}

for link in tqdm(final_array):
    try:
        if "/p/" in link:
            id_post = link.split('/')[-2]
            print(link, id_post)

            response = requests.get(link, headers=headers, params=params)
            json_response = response.json()
            
            # Num comments
            comm = json_response["graphql"]["shortcode_media"]["edge_media_preview_comment"]["count"]
            
            # Num likes
            like = json_response["graphql"]["shortcode_media"]["edge_media_preview_like"]["count"]
            
            # Is video
            is_video = json_response["graphql"]["shortcode_media"]["is_video"]
            
            # Text Description
            text_des = json_response["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
            
            #Video link
            image_link = json_response["graphql"]["shortcode_media"]["display_url"]
            
            #time of video
            time_image = json_response["graphql"]["shortcode_media"]["taken_at_timestamp"]
            
            comments[id_post] = comm
            likes[id_post] = like
            video[id_post] = is_video
            text[id_post] = text_des
            json_data[id_post] = {
                "id": id_post,
                "num_likes": like,
                "num_comments": comm,
                "is_video": is_video,
                "text_des":text_des,
                "image_link":image_link,
                "time_stamp":time_image
            }
            json_response_dict[id_post] = json_response
            
    except Exception as e:
        print("Exception",e)
        pass

os.makedirs(args.output_dir, exist_ok=True)
output_path = os.path.join(args.output_dir, args.hashtag + ".json")

with open(output_path,'w') as f:
    json.dump(json_data, f, indent=4)
