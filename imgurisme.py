import configparser
import os
import shutil
import re

import requests
from imgurpython import ImgurClient


IS_IMAGE = re.compile("^.+\.(png|jpg|jpeg|gif)$", re.IGNORECASE)


## imgur wrapper
def authenticate(username, use_credentials, config):
    client = ImgurClient(**use_credentials)

    # Authorization flow, pin example (see docs for other auth types)
    authorization_url = client.get_auth_url('pin')

    print("Go to the following URL: {0}".format(authorization_url))

    # Read in the pin, handle Python 2 or 3 here.
    pin = input("Enter pin code:")

    # ... redirect user to `authorization_url`, obtain pin (or code or token) ...
    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

    print(f"  .. caching {username} credentials")
    with open("auth_cache.ini", "w") as auth_cache:
        config["credentials"]["username"] = username
        config["credentials"]["access_token"] = credentials['access_token']
        config["credentials"]["refresh_token"] = credentials['refresh_token']
        config.write(auth_cache)
        print("saved to cache")

    return client


def load_client(config):
    credentials = dict()

    if config.has_section("credentials"):
        username = config.get("credentials", "username")
        credentials["client_id"] = config.get("credentials", "client_id")
        credentials["client_secret"] = config.get("credentials", "client_secret")
        credentials["access_token"] = config.get("credentials", "access_token")
        credentials["refresh_token"] = config.get("credentials", "refresh_token")
        client = ImgurClient(**credentials)
        print(f"  .. loaded {username} credentials")
    else:
        print("running authentication protocol")
        username = input("Enter username:")
        credentials["client_id"] = input("Enter client id:")
        credentials["client_secret"] = input("Enter client secret:")
        client = authenticate(username, credentials, config)

    return client, username


def download_image(url, destination):
    with requests.get(url, stream=True) as stream:
        with open(destination, "wb") as output:
            shutil.copyfileobj(stream.raw, output)


def upload_image(url, destination):
    with requests.get(url, stream=True) as stream:
        with open(destination, "wb") as output:
            shutil.copyfileobj(stream.raw, output)


def sync_user_gallery(client: ImgurClient, username):
    """download user submissions, to image repository"""

    home_folder = os.path.expanduser("~")
    repo_folder = os.path.join(home_folder, "Pictures", "imgurisme")

    print(f" .. scanning {repo_folder} ... ", end="")
    local_images = {filename for filename in os.listdir(repo_folder) if IS_IMAGE.match(filename)}
    print(f"found {len(local_images)} images")

    print(f" .. scanning {username} repository ...", end="")
    remote_images = dict()
    imgur_data = client.get_account_images(username)
    for item in imgur_data:
        if item.type.startswith("image"):
            filename = os.path.basename(item.link)
            remote_images[filename] = item
    print(f"found {len(remote_images)} images")

    missing_remote = local_images - remote_images.keys()
    print(f"{missing_remote=}")
    for filename in missing_remote:
        filepath = os.path.join(repo_folder, filename)
        print(" uploading ... ", filepath)
        response_data = client.upload_from_path(filepath, anon=False)
        print(f"{response_data=}")

        new_filename = os.path.basename(response_data["link"])
        new_filepath = os.path.join(repo_folder, new_filename)
        print(f"{new_filepath=}")
        download_image(response_data["link"], new_filepath)

        print(f"delete {filepath=}")
        os.remove(filepath)

    missing_local = remote_images.keys() - local_images
    print(f"{missing_local=}")
    for filename in missing_local:
        filepath = os.path.join(repo_folder, filename)
        print("should download", filepath)
        item = remote_images[filename]
        download_image(item.link, filepath)


if __name__ == "__main__":
    # cwd = os.getcwd()

    auth_cache = configparser.ConfigParser()
    auth_cache.read("auth_cache.ini")
    client, username = load_client(auth_cache)

    sync_user_gallery(client, username)

    # os.chdir(cwd)
