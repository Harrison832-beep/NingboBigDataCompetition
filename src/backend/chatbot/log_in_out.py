from backend import settings
import requests  # pip3 install requests


def get_login_info(code):
    code_url = settings.code2Session.format(settings.AppId, settings.AppSecret, code)
    response = requests.get(code_url)
    json_response = response.json()  # turn into json library
    if json_response.get("session_key"):
        return json_response
    else:
        return False
