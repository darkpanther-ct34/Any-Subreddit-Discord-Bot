import praw
import random
import discord
import prawcore.exceptions
# from discord.ext import commands
# import requests
import requests.auth
import os
from dotenv import load_dotenv
load_dotenv()

user_agent = "Discord_bot/0.1 by Discord_bot_7667"


ID = os.getenv('client_id')
secret = os.getenv('client_secret')

username = os.getenv('reddit_username')
password = os.getenv('reddit_password')


client_auth = requests.auth.HTTPBasicAuth(ID, secret)
post_data = {"grant_type": "password", "username": username, "password": password}
headers = {"User-Agent": user_agent}
response = requests.post("https://www.reddit.com/api/v1/access_token",
                         auth=client_auth,
                         data=post_data,
                         headers=headers
                         )
response.json()

authorisation_token = response.json()["token_type"]+' '+response.json()["access_token"]
headers = {"Authorization": authorisation_token, "User-Agent": user_agent}
response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
response.json()

reddit = praw.Reddit(
    client_id=ID,
    client_secret=secret,
    user_agent=user_agent,
    check_for_async=False
)


def any_sub(message, nsfw):
    try:
        posts = []
        for submission in reddit.subreddit(message).hot(limit=10):
            if not submission.stickied:
                posts.append({"author": str(submission.author),
                              "URL for img": submission.url,
                              "URL": ("https://www.reddit.com" + submission.permalink),
                              "title": submission.title,
                              "text": submission.selftext,
                              "nsfw": submission.over_18})
        chosen_post = random.choice(posts)
        if nsfw == "False":
            counter = 0
            while counter < 10:
                chosen_post = posts[counter]
                if not chosen_post["nsfw"]:
                    break
                counter += 1
            if not chosen_post["nsfw"]:
                print("Fine")
                image_url = chosen_post["URL for img"]
                embed_var = discord.Embed(title=chosen_post["title"],
                                          url=chosen_post["URL"],
                                          description=chosen_post['text'],
                                          colour=0x3CA47C)
                embed_var.set_image(url=image_url)
                embed_var.set_author(name=chosen_post["author"],
                                     icon_url=(reddit.redditor(chosen_post["author"])).icon_img)
            else:
                print("NSFW")
                embed_var = discord.Embed(title="Failed Command",
                                          description="That sub was NSFW. "
                                                      "You can change your settings using the !nsfw command",
                                          color=0xFF0000)
        else:
            image_url = chosen_post["URL for img"]
            embed_var = discord.Embed(title=chosen_post["title"],
                                      url=chosen_post["URL"],
                                      description=chosen_post['text'],
                                      colour=0x3CA47C)
            embed_var.set_image(url=image_url)
            embed_var.set_author(name=chosen_post["author"], icon_url=(reddit.redditor(chosen_post["author"])).icon_img)
    except prawcore.exceptions.Forbidden:
        embed_var = discord.Embed(title="Failed Command", description="That subreddit doesn't exist", color=0xFF0000)
    except prawcore.exceptions.BadRequest:
        embed_var = discord.Embed(title="Failed Command", description="That subreddit doesn't exist", color=0xFF0000)
    return embed_var
