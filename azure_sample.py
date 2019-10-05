#! /usr/bin/env python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import os
import sys
import time

# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Recognize text with the Read API in a remote image by:
#   1. Specifying whether the text to recognize is handwritten or printed.
#   2. Calling the Computer Vision service's batch_read_file_in_stream with the:
#      - context
#      - image
#      - text recognition mode
#   3. Extracting the Operation-Location URL value from the batch_read_file_in_stream
#      response
#   4. Waiting for the operation to complete.
#   5. Displaying the results.
remote_image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjr2CsAcRyzcdC9yFeC5OMLbipxGppQNLV7cyFL_OtwYa5b7IRPg"
text_recognition_mode = TextRecognitionMode.printed
num_chars_in_operation_id = 36

client_response = computervision_client.batch_read_file(remote_image_url, {}, raw=True)

operation_location = client_response.headers["Operation-Location"]
id_location = len(operation_location) - num_chars_in_operation_id
operation_id = operation_location[id_location:]

print("\nRecognizing text in a remote image with the batch Read API ... \n")

while True:
    result = computervision_client.get_read_operation_result(operation_id)
    if result.status not in ['NotStarted', 'Running']:
        break
    time.sleep(1)

if result.status == TextOperationStatusCodes.succeeded:
    for text_result in result.recognition_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
            print()