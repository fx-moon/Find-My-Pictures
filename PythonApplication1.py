#!/usr/bin/env python
# coding: utf-8

import asyncio
import aiohttp
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-q", help="input query word", type=str)
args = parser.parse_args()

#configure
subscription_key = "408f9d1576fc44e5b7606fd911d0c5e8"
assert subscription_key
vision_base_url = "https://team17.cognitiveservices.azure.com/vision/v2.0/"
analyze_url = vision_base_url + "describe"

#init
maxConnection=10
conn=0
target=[]
tasks = []
image_path='/Users/vincent/Pictures/pics/'
dirs = os.listdir(image_path)
query = args.q
print("query: ",query)

async def GetImInfo(image_path):
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    if conn > maxConnection:
        asyncio.sleep(1)
    async with aiohttp.request(method='post',url=analyze_url,headers=headers,params=params,data=image_data) as r:
        analysis = await r.json()

    print(analysis["description"]["tags"])
    if query in analysis["description"]["tags"]:
        target.append(image_path)

for img in dirs:
    if os.path.splitext(img)[1] in [".jpeg",".jpg",".png"]:
        path = image_path + img
        #print(path)
        tasks.append(GetImInfo(path))

event_loop = asyncio.get_event_loop()
results = event_loop.run_until_complete(asyncio.gather(*tasks))
event_loop.close()

print(target)