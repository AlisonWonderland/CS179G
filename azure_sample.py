#! /usr/bin/env python
import os
import requests
import time
import json
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO

# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

analyze_url = endpoint + "vision/v2.1/read/core/asyncBatchAnalyze"

for f_name in os.listdir('./'):
    if f_name.endswith('.jpg'):
        # print(f_name)
        # Set image_path to the local path of an image that you want to analyze.
        image_path = f_name

        print("--------------------" + image_path + "--------------------")

        # Read the image into a byte array
        image_data = open(image_path, "rb").read()
        headers = {'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/octet-stream'}
        params = {'visualFeatures': 'Categories,Description,Color'}
        response = requests.post(
            analyze_url, headers=headers, params=params, data=image_data)
        # response.raise_for_status()

        # Holds the URI used to retrieve the recognized text.
        # print("op location: ", response.headers["Operation-Location"])
        # operation_url = response.headers["Operation-Location"]
        print("headers: ", response.headers)

        while("Retry-After" in response.headers):
            time.sleep(int(response.headers['Retry-After']) + 1)
            response = requests.post(
            analyze_url, headers=headers, params=params, data=image_data)

        # The recognized text isn't immediately available, so poll to wait for completion.
        analysis = {}
        poll = True
        while (poll):
            response_final = requests.get(
                response.headers["Operation-Location"], headers=headers)
            analysis = response_final.json()
            time.sleep(1)
            if ("recognitionResults" in analysis):
                poll = False
            if ("status" in analysis and analysis['status'] == 'Failed'):
                poll = False

        for j in range(len(analysis["recognitionResults"][0]["lines"])):
            print(analysis["recognitionResults"][0]["lines"][j]["text"])