import requests
import configparser
import json

url = "https://osu.ppy.sh/oauth/token"


def open_token(request):  # return token into config file
    token_config = configparser.ConfigParser()
    try:
        token_config.read("Tokens.ini")
        token_config.get("Tokens", "access_token")
    except Exception as e:
        print(e)
        answer = input("Token file corrupted or not found. Create again? (y/n)")
        if answer == "y":
            open("Tokens.ini", "w")
            token_config.add_section("Tokens")
            token_config.set("Tokens", "access_token", "<write access_token here manually>")
            token_config.set("Tokens", "refresh_token", "<write refresh_token here manually>")

            with open("Tokens.ini", "w") as file:
                token_config.write(file)

            print("New file created")
        else:
            print("ok")

    if request == "get_token":
        return token_config.get("Tokens", "access_token")
    elif request == "get_refresh_token":
        return token_config.get("Tokens", "refresh_token")


def write_token(access_token, refresh_token):
    token_config = configparser.ConfigParser()
    token_config.read("tokens.ini")

    token_config.set("Tokens", "access_token", access_token)
    token_config.set("Tokens", "refresh_token", refresh_token)
    with open("Tokens.ini", "w") as file:
        token_config.write(file)

    print("Oauth tokens refreshed")


def refresh_access_token():
    response = requests.post(url,
                             data={'grant_type': 'refresh_token',
                                   'client_id': '<id>',
                                   'client_secret': '<client_secret_code>',
                                   'redirect_uri': 'https://example.com',
                                   'refresh_token': f'{open_token("get_refresh_token")}'
                                   },
                             headers={
                                 'Content-Type': 'application/x-www-form-urlencoded',
                                 'Accept': 'application/json',
                                 'Authorization': 'Bearer'})
    data = json.loads(response.text)

    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    write_token(access_token, refresh_token)