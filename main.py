import json
from instagrapi import Client

with open('data.json', 'r') as file:
    data = json.load(file)
    username = data['username']
    password = data['password']

client = Client()
client.login(username, password)
print(f"Logged in as {username}.")

followers = client.user_followers(client.user_id)
followers_dict = {user.pk: user.username for user in followers.values()}
print(f"{username} has {len(followers)} followers.")
print("Followers:")
print(json.dumps(followers_dict, indent=4))

followings = client.user_following(client.user_id)
followings_dict = {user.pk: user.username for user in followings.values()}
print(f"{username} is following {len(followings)} users.")
print("Followings:")
print(json.dumps(followings_dict, indent=4))

nonfollowers = {pk: username for pk, username in followings_dict.items() if pk not in followers_dict}
print(f"{username} has {len(nonfollowers)} nonfollowers.")
print("Nonfollowers:")
print(json.dumps(nonfollowers, indent=4))

for pk, username in nonfollowers.items():
    print(f"Nonfollower PK: {pk}, Username: {username}")