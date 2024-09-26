from instagrapi import Client

client = Client()

def login(username, password):
    client.login(username, password)
    return "Login successful"

def get_followers():
    followers = client.user_followers(client.user_id)
    followers_dict = {user.pk: user.username for user in followers.values()}
    return followers_dict

def get_followings():
    followings = client.user_following(client.user_id)
    followings_dict = {user.pk: {'username': user.username, 'profile_pic_url': str(user.profile_pic_url)} for user in followings.values()}
    return followings_dict

def determine_nonfollowers(followers_dict, followings_dict):
    nonfollowers = [
        {'pk': pk, 'username': user_info['username'], 'profile_pic_url': user_info['profile_pic_url']}
        for pk, user_info in followings_dict.items() if pk not in followers_dict
    ]
    return nonfollowers