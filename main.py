import os
import requests
import random

# from instapy_cli import client
from instabot import Bot
from dotenv import load_dotenv

from download_image import download_image
from generate_image import generate_quotes_image

load_dotenv(verbose=True)

username = os.getenv('INSTA_USERNAME')
password = os.getenv('INSTA_PASSWORD')


hashtags = [
    'motivation',
    'inspiring',
    'lifestyle',
    'success',
    'goals',
    'hardships',
    'entrepreneurs',
    'happiness',
    'positive',
    'motivational',
    'life',
    'travel',
    'positivevibes',
    'hustle',
    'books',
    'reader'
]

quotes_url = 'http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en'

success = False
while success == False:
    response = requests.get(quotes_url)
    if response.status_code == 200:
        quote_json = response.json()
        quote = quote_json['quoteText'] + ' -' + quote_json['quoteAuthor']
        success = True

filename = download_image()
image_path = './images/'+filename
print(filename)
processed_image = generate_quotes_image(image_path, quote)

text_caption = quote + '\n\n\n'

stop = False
temp_hashtags = []
while stop == False:
    index = random.randint(0,len(hashtags)-1)
    if(hashtags[index] in temp_hashtags):
        continue
    if(len(temp_hashtags) >= 10):
        break
    temp_hashtags.append(hashtags[index])
    stop = True

for hashtag in hashtags:
    text_caption += ('#' + hashtag + ' ')

print(text_caption)

# with client(username, password) as cli:
#     cli.upload(processed_image, text_caption)
bot = Bot()
bot.login(username=username, password=password)
bot.upload_photo(processed_image, text_caption)
os.rename(processed_image + '.REMOVE_ME', processed_image)