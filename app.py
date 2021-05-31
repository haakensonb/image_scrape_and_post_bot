import praw
import requests
import random
import imagehash
from PIL import Image
import os
from secrets import REDDIT_ID, REDDIT_SECRET, REDDIT_USER_AGENT

DIR = "images"
if not os.path.exists(DIR):
    os.makedirs(DIR)

if __name__ == "__main__":
    print("Hello World")
    reddit = praw.Reddit(
        client_id = REDDIT_ID,
        client_secret = REDDIT_SECRET,
        user_agent = REDDIT_USER_AGENT
    )
    posts = [post for post in reddit.subreddit("LiminalSpace").hot(limit=25)]
    filtered_posts = [post for post in posts if post.url.startswith("https://i.")]
    post = random.choice(filtered_posts)
    file_loc = f"./{DIR}/{post.title}.jpg"
    with open(file_loc, "wb") as f:
        f.write(requests.get(post.url).content)
    img_hash = imagehash.phash(Image.open(file_loc))
    print(img_hash)