import json
import requests
import utils
import datetime

twitchConfig = utils.twitchconfig()

def get_app_access_token():
    params = {
        "client_id": twitchConfig["client_id"],
        "client_secret": twitchConfig["client_secret"],
        "grant_type": "client_credentials"
    }

    response = requests.post(
        "https://id.twitch.tv/oauth2/token", params=params)
    print(response.json())
    access_token = response.json()["access_token"]
    return access_token


def get_users(login_names):
    params = {
        "login": login_names
    }

    headers = {
        "Authorization": "Bearer {}".format(twitchConfig["access_token"]),
        "Client-Id": twitchConfig["client_id"]
    }

    response = requests.get(
        "https://api.twitch.tv/helix/users", params=params, headers=headers)
    return {entry["login"]: entry["id"] for entry in response.json()["data"]}


def get_streams(users):
    params = {
        "user_id": users.values()
    }

    headers = {
        "Authorization": "Bearer {}".format(twitchConfig["access_token"]),
        "Client-Id": twitchConfig["client_id"]
    }

    response = requests.get(
        "https://api.twitch.tv/helix/streams", params=params, headers=headers)
    return {entry["user_login"]: entry for entry in response.json()["data"]}


online_users = {}

def get_notifications():
    watchlist = []

    if ("watchlist" not in twitchConfig):
        return []

    raw_watchlist = twitchConfig["watchlist"]

    # filter watchlist for duplicates
    for i in raw_watchlist:
        if i in list:
            pass
        else:
            list.append(i)

    streams = get_streams(get_users(list))

    notifications = []

    for user_name in watchlist:
        if user_name not in online_users:
            online_users[user_name] = datetime.datetime.utcnow()

        if user_name not in streams:
            online_users[user_name] = None
        else:
            started_at = datetime.datetime.strptime(
                streams[user_name]["started_at"], "%Y-%m-%dT%H:%M:%SZ")
            if online_users[user_name] is None or started_at > online_users[user_name]:
                notifications.append(streams[user_name])
                online_users[user_name] = started_at

    return notifications
