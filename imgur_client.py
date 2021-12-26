import base64
import configparser
import os
import re
import shutil
import subprocess

import requests


def exec(command):
    """runs shell command and capture the output"""
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode:
        print(f"Error executing: {command}")
        raise RuntimeError(result.stderr.decode("utf-8").strip())

    return result.stdout.decode("utf-8").strip()


class ImmutableData(dict):
    """Read only attribute dictionary"""

    def __getattr__(self, attr):
        return self[attr]

    def __hash__(self):
        return id(self)

    def _immutable_error(self, *args, **kws):
        raise TypeError("Cannot modify immutable data")

    __delete__ = _immutable_error
    __setattr__ = _immutable_error
    __setitem__ = _immutable_error
    __delitem__ = _immutable_error
    clear = _immutable_error
    update = _immutable_error
    setdefault = _immutable_error
    pop = _immutable_error
    popitem = _immutable_error


class ImgurClient:
    """Yet another Imgur client, python this time"""

    API_ROOT = "https://api.imgur.com"
    API_V3 = "https://api.imgur.com/3"
    AUTH_CACHE = "auth_cache.ini"
    ANY_NON_WORD = re.compile("[\W_\s]+")

    def __init__(self):
        """
        Reads refresh token from auth cache and gets a new token.
        If no credentials are found, then creates an empty config file.
        If only the refresh token is missing it triggers the whole application
        authorization flow.
        At the end of each successful authorization or token refresh the new
        credentials are saved to the auth_cache file.
        """

        if os.path.isfile(self.AUTH_CACHE):
            auth_cache = configparser.ConfigParser()
            auth_cache.read(self.AUTH_CACHE)
        else:
            # create empty file
            empty_credentials = dict(client_id="", client_secret="")
            self.cache_credentials(empty_credentials)
            raise RuntimeError(f"Created empty {self.AUTH_CACHE}, please fill in")

        credentials = dict()
        credentials["client_id"] = auth_cache.get("credentials", "client_id")
        credentials["client_secret"] = auth_cache.get("credentials", "client_secret")
        credentials["refresh_token"] = auth_cache.get(
            "credentials", "refresh_token", fallback=None
        )

        data = self.authenticate(credentials)

        self.token = data["access_token"]
        self.username = data["account_username"]
        self.account_id = data["account_id"]
        self.auth_headers = dict(Authorization=f"Bearer {self.token}")

        credentials["refresh_token"] = data.pop("refresh_token")
        self.cache_credentials(credentials)
        print(f"- authenticated as {self.username}")

    def cache_credentials(self, credentials):
        """Saves provided credentials to auth cache file"""
        with open(self.AUTH_CACHE, "w") as storage:
            auth_cache = configparser.ConfigParser()
            auth_cache["credentials"] = credentials
            auth_cache.write(storage)

    def authorize(self, client_id, client_secret):
        """Starts the authorization flow with imgur"""
        print("- launching browser to authorize application access")
        url = (
            f"{self.API_ROOT}/oauth2/authorize?client_id={client_id}&response_type=pin"
        )
        exec(f"xdg-open '{url}'")

        pin = input("Enter PIN code:")

        route = "oauth2/token"
        url = f"{self.API_ROOT}/{route}"
        payload = dict(
            client_id=client_id,
            client_secret=client_secret,
            grant_type="pin",
            pin=pin,
        )

        response = requests.post(url, payload)

        response.raise_for_status()
        return response.json()

    def get_access_token(self, credentials):
        """Having a refresh token, gets an access_token"""
        route = "oauth2/token"
        payload = dict(
            **credentials,
            grant_type="refresh_token",
        )
        url = f"{self.API_ROOT}/{route}"

        response = requests.post(url, payload)

        response.raise_for_status()
        return response.json()

    def authenticate(self, credentials):
        """Attempts authentication with given credentials"""
        if credentials["refresh_token"] is None:
            del credentials["refresh_token"]
            accees_data = self.authorize(**credentials)
        else:
            accees_data = self.get_access_token(credentials)
        return accees_data

    def api_get(self, api, params=None, data=None):
        """
        Runs a GET request to imgur api.
        On success it returns an ImmutableData object, to allow accessing
        dictionary response keys as attributes.
        On failure it raises apropriate HttpErrors.
        """
        url = f"{self.API_V3}/{api}"

        response = requests.get(url, params, data=data, headers=self.auth_headers)

        response.raise_for_status()
        response_data = response.json()["data"]

        if isinstance(response_data, dict):
            return ImmutableData(response_data)
        elif isinstance(response_data, list):
            return (ImmutableData(item) for item in response_data)

        # a bit unexpected, but hey... let's take it
        return response_data

    def api_post(self, api, data=None):
        """
        Runs a GET request to imgur api.
        On success it returns an ImmutableData object, to allow accessing
        dictionary response keys as attributes.
        On failure it raises apropriate HttpErrors.
        """
        url = f"{self.API_V3}/{api}"

        response = requests.post(url, data=data, headers=self.auth_headers)

        response.raise_for_status()
        response_data = response.json()["data"]

        if isinstance(response_data, dict):
            return ImmutableData(response_data)
        elif isinstance(response_data, list):
            return (ImmutableData(item) for item in response_data)

        # a bit unexpected, but hey... let's take it
        return response_data

    def me(self):
        """Get current user details"""
        api_url = f"account/{self.username}"
        return self.api_get(api_url)

    def list_submissions(self, page=0, sort="newest"):
        """
        Gets all image submissions to the gallery.

        Keyword arguments:
        page -- which page to retrieve, for larger results (default: 0)
        sort -- newest (default), oldest, worst, best.
        """
        api_url = f"account/{self.username}/submissions/{page}/{sort}"
        return self.api_get(api_url)

    def list_images(self):
        """Gets all uploaded images"""
        api_url = "account/me/images"
        return self.api_get(api_url)

    def get_image(self, image_id, username=None):
        """Having an image id it grabs all image details"""
        if username is None:
            username = "me"
        api_url = f"account/{username}/image/{image_id}"
        return self.api_get(api_url)

    def upload_image(self, filepath, title=None, description=None):
        """upload image from path, will load the entire file in memory, lame"""

        with open(filepath, "rb") as file:
            content = base64.b64encode(file.read())

        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)
        title = re.sub(self.ANY_NON_WORD, " ", name).strip().title()
        payload = dict(
            image=content,
            type="base64",
            name=filename,
            title=title,
            description=description,
        )

        return self.api_post(api="image", data=payload)

    def download_image(self, url, destination):
        with requests.get(url, stream=True) as stream:
            with open(destination, "wb") as output:
                shutil.copyfileobj(stream.raw, output)


if __name__ == "__main__":
    client = ImgurClient()

    user = client.me()
    print(user.id, user.url, user.reputation_name, user.reputation)

    submissions = client.list_submissions()
    for i, img in enumerate(submissions):
        print(i, img.title, img.views, img.points, img.link)

    images = client.list_images()
    for i, img in enumerate(images):
        print(i, img.id, img.title, img.views, img.link)
