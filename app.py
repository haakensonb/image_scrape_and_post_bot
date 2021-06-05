from config import DB_FILENAME, DB_PATH
from utils import get_session
import praw
import requests
import random
import imagehash
from PIL import Image
import os
import tweepy
from models.ImgRecord import ImgRecord
from secrets import REDDIT_ID, REDDIT_SECRET, REDDIT_USER_AGENT, TWIT_KEY, TWIT_SECRET, TWIT_ACCESS_TOKEN, TWIT_ACCESS_SECRET

DIR = "images"
if not os.path.exists(DIR):
    os.makedirs(DIR)


class TwitterWrapper():
    def __init__(self, key=TWIT_KEY, secret=TWIT_SECRET, access_token=TWIT_ACCESS_TOKEN, access_secret=TWIT_ACCESS_SECRET):
        self.key = key
        self.secret = secret
        self.access_token = access_token
        self.access_secret = access_secret
        self.auth = tweepy.OAuthHandler(self.key, self.secret)
        self.auth.set_access_token(self.access_token, self.access_secret)
        self.api = tweepy.API(self.auth)

    def post_img(self, post_title, file_name, img_src_link, file_dir = "./images"):
        img_path = f"{file_dir}/{file_name}.jpg" 
        img = self.api.media_upload(img_path)
        tweet = f"'{post_title}' Source: {img_src_link} #liminal #liminalspaces"
        self.api.update_status(status=tweet, media_ids=[img.media_id])
        print("Image posted")

if __name__ == "__main__":
    reddit = praw.Reddit(
        client_id=REDDIT_ID,
        client_secret=REDDIT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    posts = [post for post in reddit.subreddit("LiminalSpace").hot(limit=100)]
    filtered_posts = [
        post for post in posts if post.url.startswith("https://i.")]
    post = random.choice(filtered_posts)
    post_permalink = f"https://reddit.com{post.permalink}"
    file_loc = f"./{DIR}/temp.jpg"
    with open(file_loc, "wb") as f:
        f.write(requests.get(post.url).content)
    img_hash = str(imagehash.phash(Image.open(file_loc)))
    print(f"image hash: {img_hash}")
    img_record = ImgRecord(id=img_hash, link=post_permalink)
    try:
        s = get_session()
        exists = s.query(ImgRecord.id).filter_by(id=img_hash).first()

        if not exists:
            print("New image hash added")
            # File will be permanent so rename it
            new_file_loc = f"./{DIR}/{img_hash}.jpg"
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

    twit = TwitterWrapper()
    twit.post_img(post.title, img_hash, post_permalink)
