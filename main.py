import json
from instagrapi import Client

def get_nonfollowers(username, password):
    client = Client()
    client.login(username, password)

    # Get followers and following
    followers = client.user_followers(client.user_id)
    followers_dict = {user.pk: user.username for user in followers.values()}

    followings = client.user_following(client.user_id)
    followings_dict = {user.pk: user.username for user in followings.values()}

    # Determine non-followers
    nonfollowers = [username for pk, username in followings_dict.items() if pk not in followers_dict]
    return nonfollowers