import requests
import json
import TokenRefresh

token = TokenRefresh.open_token("get_token")


def account_data(username):
    response = requests.get(f"https://osu.ppy.sh/api/v2/users/{username}/",
                            headers={"Content-Type": "application/json",
                                     "Accept": "application/json",
                                     "Authorization": f"Bearer {token}"})
    return json.loads(response.text)


def write_json(data):  # for develop
    with open("json.json", "w") as file:
        file.write(data)


def best_scores(user_id, limit=1):
    response = requests.get(f"https://osu.ppy.sh/api/v2/users/{user_id}/scores/best/?&limit={limit}",
                            headers={"Content-Type": "application/json",
                                     "Accept": "application/json",
                                     "Authorization": f"Bearer {token}"})

    return json.loads(response.text)


def recent_scores(user_id, limit=1):
    response = requests.get(f"https://osu.ppy.sh/api/v2/users/{user_id}/scores/recent/?&limit={limit}",
                            headers={"Content-Type": "application/json",
                                     "Accept": "application/json",
                                     "Authorization": f"Bearer {token}"})

    return json.loads(response.text)


def is_fc(data, index=0):  # meh
    if data[index]["perfect"]:
        return True


def get_username(username):
    data = account_data(username)
    name = data["username"]
    return str(name)


def get_pp(username):
    data = account_data(username)
    pp = int(data["statistics"]["pp"])
    return str(pp)


def get_rank(username):
    data = account_data(username)
    rank = data["statistics"]["pp_rank"]
    return str(rank)


def get_accuracy(username):
    data = account_data(username)
    accuracy = data["statistics"]["hit_accuracy"]
    return str(accuracy)


def get_play_count(username):
    data = account_data(username)
    play_count = data["statistics"]["play_count"]
    return str(play_count)


def short_info(username, new_user):
    data = account_data(username)
    print(data)
    name = data["username"]
    pp = int(data["statistics"]["pp"])
    play_count = data["statistics"]["play_count"]
    rank = data["statistics"]["pp_rank"]

    if new_user == "new_user":
        return f"{name}, нафармил {pp}pp за {play_count} игр. Ранк #{rank}"
    elif new_user == "old_user":
        return f"{name}, нафармил {pp}pp за {play_count} игр. Ранк #{rank}"
