# All Sparks Assignment 2

from google.cloud import vision
from google.cloud.vision import types
import os
import io
import base64
import re
import json
from google.protobuf.json_format import MessageToJson



def gatherData(path):
  client = vision.ImageAnnotatorClient()

  with io.open(path, 'rb') as image_file:
      content = image_file.read()

  image = vision.types.Image(content=content)
  response = client.text_detection(image=image)
  sr = json.loads(MessageToJson(response))
  texts = sr['textAnnotations'][0]['description'] #.split('\n')

  dictUserData = {
                  'name': "Not Found",
                  'lab no': "Not Found",
                  'age': 'Not Found',
                  'gender': "Not Found",
                  'ref by': "Not Found",
              }

  keys = list(dictUserData.keys())


  for dict_key in keys:
    if re.search(dict_key,texts.lower()):
        span = re.search(dict_key,texts.lower()).span()
        temp = ""
        flag = 0
        for i in range(span[1]+1,len(texts)):   ##
            if "\n" in texts[i] and flag==1:
              flag = 0
              texts = texts.replace( texts[span[0]:i ],'')
              break
            else:
              flag = 1
            temp = temp + texts[i].replace('\n','')
        dictUserData.update({dict_key:temp})

  texts = texts.split('\n')
  for i in range(1,len(texts)):
    if bool(re.findall('\d+',texts[i-1])) == False and len(texts[i-1]) > 1:
      try:
        if texts[i][0].isdigit():
          dictUserData.update({ texts[i-1]:texts[i] })
      except:
          pass

  return dictUserData


path = input("Enter the path to the key file ~key.json:\n")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=path

path = input("Enter the path of receipt image:\n")
res = gatherData(path)
print('\n',res)



          
