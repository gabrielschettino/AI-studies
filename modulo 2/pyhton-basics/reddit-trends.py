import requests
import pandas as pd
from collections import defaultdict
from nltk.corpus import stopwords
import nltk
import pickle
from dotenv import load_dotenv
import os

load_dotenv()
nltk.download('stopwords')


# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(
    'TXIYR30vRClP8g7qXQT5tA', 'ftqjZImkIrmLZ7wsCe5XfxxsU_ODBA')

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': os.getenv("REDDIT_USERNAME"),
        'password': os.getenv("REDDIT_PASSWORD")}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

print(res.json())  # let's see what we get

df = pd.DataFrame()  # initialize dataframe
after = None  # initialize 'after' parameter

# Create a dictionary to store word frequencies
word_freq = defaultdict(int)
i = 0


for i in range(0, 100):
    # Modify the URL to include the 'after' parameter
    url = "https://oauth.reddit.com/r/cosplay"
    if after:
        url += "?after=" + after

    res = requests.get(url, headers=headers)
    data = res.json()

    # loop through each post retrieved from GET request
    for post in data['data']['children']:
        post_data = {
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
            'date': post['data']['created_utc']
        }

        # append post data to dataframe
        df = df._append(post_data, ignore_index=True)

    # Check if there are more posts to retrieve
    after = data['data']['after']
    if not after:
        break

df['date'] = pd.to_datetime(df['date'], unit='s')
# remove rows with posts made before 2023
# df = df[df['date'].dt.year >= 2023]

print(df)

pickle.dump(df, open('cosplay.xxx', 'wb'))
