from config import DB_FILENAME, DB_PATH
from utils import get_session
import praw
import requests
import random
import imagehash
from PIL import Image
import os

from models.ImgRecord import ImgRecord
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
    file_loc = f"./{DIR}/temp.jpg"
    with open(file_loc, "wb") as f:
        f.write(requests.get(post.url).content)
    img_hash = str(imagehash.phash(Image.open(file_loc)))
    print(f"image hash: {img_hash}")
    img_record = ImgRecord(id=img_hash)
    try:
        s = get_session()
        exists = s.query(ImgRecord.id).filter_by(id=img_hash).first()

        if not exists:
            print("New image hash added")
            # File will be permanent so rename it
            new_file_loc = f"./{DIR}/{post.title}.jpg"
            os.rename(file_loc, new_file_loc)
            s.add(img_record)
            s.commit()
        else:
            print("Duplicate image")
            # Don't need a duplicate img
            os.remove(file_loc)

    except:
        s.rollback()
        raise
    
    finally:
        s.close()