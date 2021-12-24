import configparser
import subprocess
import re
import os
import requests


IS_IMAGE = re.compile("^.+\.(png|jpg|jpeg|gif)$", re.IGNORECASE)


def exec(command):
    """runs shell command and capture the output"""
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode:
        print(f"Error executing: {command}")
        raise RuntimeError(result.stderr.decode("utf-8").strip())

    return result.stdout.decode("utf-8").strip()


class ImgurClient:
    """Yet another Imgur client, python this time"""

    API_ROOT = "https://api.imgur.com"
    API_V3 = "https://api.imgur.com/3"
    AUTH_CACHE = "auth_cache.ini"

    def __init__(self):
        if os.path.isfile(self.AUTH_CACHE):
            auth_cache = configparser.ConfigParser()
            auth_cache.read(self.AUTH_CACHE)
        else:
            # create empty file
            empty_credentials = dict(client_id = "", client_secret = "")
            self.cache_credentials(empty_credentials)
            raise RuntimeError(f"Created empty {self.AUTH_CACHE}, please fill in")

        credentials = dict()
        credentials["client_id"] = auth_cache.get("credentials", "client_id")
        credentials["client_secret"] = auth_cache.get("credentials", "client_secret")
        credentials["refresh_token"] = auth_cache.get("credentials", "refresh_token", fallback=None)

        data = self.authenticate(credentials)
        self.token = data["access_token"]
        assert self.token

    def cache_credentials(self, credentials):
        with open(self.AUTH_CACHE, "w") as storage:
            auth_cache = configparser.ConfigParser()
            auth_cache["credentials"] = credentials
            auth_cache.write(storage)
            print(f"- saved authorisation to {self.AUTH_CACHE}")

    def authorize(self, client_id, client_secret):
        route = "oauth2/authorize"
        print("- launching browser to authorize application access")
        url = f"{self.API_ROOT}/{route}?client_id={client_id}&response_type=pin"
        exec(f"xdg-open \'{url}\'")

        pin = input("Enter PIN code:")
        route = "oauth2/token"
        url = f"{self.API_ROOT}/{route}"
        params = dict(
            client_id=client_id,
            client_secret=client_secret,
            grant_type="pin",
            pin=pin,
        )
        response = requests.post(url, params)

        assert response.status_code == 200
        access_data = response.json()
        return access_data

    def get_access_token(self, credentials):
        route = "oauth2/token"
        payload = dict(
            **credentials,
            grant_type="refresh_token",
        )
        url = f"{self.API_ROOT}/{route}"
        response = requests.post(url, payload)

        assert response.status_code == 200
        access_data = response.json()
        return access_data

    def authenticate(self, credentials):
        if credentials["refresh_token"] is None:
            del credentials["refresh_token"]
            accees_data = self.authorize(**credentials)
        else:
            accees_data = self.get_access_token(credentials)

        credentials["refresh_token"] = accees_data.pop("refresh_token")
        self.cache_credentials(credentials)

        return accees_data


if __name__ == "__main__":
    client = ImgurClient()
