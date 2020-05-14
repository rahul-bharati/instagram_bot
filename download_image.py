import os
import requests
import shutil
import random

from dotenv import load_dotenv
load_dotenv(verbose=True)

search_query = [
    'people',
    'lifestyle',
    'travel',
    'nature',
    'books'
]

def download_image():
    success = False
    while success == False:
        page_number = random.randint(1, 10)
        image_number = random.randint(0,14)
        query = random.randint(0,4)

        url = 'https://api.pexels.com/v1/search?query=' + search_query[query] + '&per_page=15&page=' + str(page_number)
        headers = {'Authorization': os.getenv('PEXELS_API_KEY')}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            success = True

            image_url = response.json()['photos'][image_number]['src']['original']
            filename = image_url.split('/')[-1]
            image_response = requests.get(image_url, stream=True)
            if image_response.status_code == 200:
                with open('./images/'+filename, 'wb') as f:
                    image_response.raw.decode_content = True
                    shutil.copyfileobj(image_response.raw, f)
    return filename
