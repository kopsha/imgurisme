import configparser
import os
import shutil
import re

import requests
from imgurpython import ImgurClient


IS_IMAGE = re.compile("^.+\.(png|jpg|jpeg|gif)$", re.IGNORECASE)


def download_image(url, destination):
    with requests.get(url, stream=True) as stream:
        with open(destination, "wb") as output:
            shutil.copyfileobj(stream.raw, output)


def sync_user_gallery(client: ImgurClient, username):
    """download user submissions, to image repository"""

    home_folder = os.path.expanduser("~")
    repo_folder = os.path.join(home_folder, "Pictures", "imgurisme")

    print(f"- scanning {repo_folder} ..", end="")
    local_images = {
        filename for filename in os.listdir(repo_folder) if IS_IMAGE.match(filename)
    }
    print(f". found {len(local_images)} images")

    print(f"- scanning {username} repository ..", end="")
    remote_images = dict()
    imgur_data = client.get_account_images(username)
    for item in imgur_data:
        if item.type.startswith("image"):
            filename = os.path.basename(item.link)
            remote_images[filename] = item
    print(f". found {len(remote_images)} images")

    missing_remote = local_images - remote_images.keys()
    print(f"{missing_remote=}")
    for filename in missing_remote:
        filepath = os.path.join(repo_folder, filename)
        print("- uploading ..", filepath, end="")
        response_data = client.upload_from_path(filepath, anon=False)

        new_image = client.get_image(response_data["id"])
        new_filename = os.path.basename(new_image.link)
        new_filepath = os.path.join(repo_folder, new_filename)
        download_image(new_image.link, new_filepath)

        print(f". done, removing {filepath}")
        os.remove(filepath)

    missing_local = remote_images.keys() - local_images
    print(f"{missing_local=}")
    for filename in missing_local:
        filepath = os.path.join(repo_folder, filename)
        print("- downloading ..", filepath)
        item = remote_images[filename]
        download_image(item.link, filepath)


if __name__ == "__main__":
    auth_cache = configparser.ConfigParser()
    auth_cache.read("auth_cache.ini")
    client, username = load_client(auth_cache)
    client.change_account_settings(username, dict(public_images="true"))

    sync_user_gallery(client, username)
    data = dict(
        title="Too much sugga",
        terms=True,
        mature=True,
        tags=["like-it-or-not"],
        is_album=False,
    )
    response = client.make_request("POST", "post/v1/posts/dCXBCjI/share", data=data)

    print(f"{response=}")
