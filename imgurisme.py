import os
import re
from imgur_client import ImgurClient


IS_IMAGE = re.compile("^.+\.(png|jpg|jpeg|gif)$", re.IGNORECASE)


def sync_user_gallery(client: ImgurClient):
    """download user submissions, to image repository"""

    home_folder = os.path.expanduser("~")
    repo_folder = os.path.join(home_folder, "Pictures", "imgurisme")

    print(f"- scanning {repo_folder} ..", end="")
    local_images = {
        filename for filename in os.listdir(repo_folder) if IS_IMAGE.match(filename)
    }
    print(f". found {len(local_images)} images")

    print(f"- scanning {client.username} repository ..", end="")
    remote_images = dict()
    imgur_data = client.list_images()
    for item in imgur_data:
        if item.type.startswith("image"):
            filename = os.path.basename(item.link)
            remote_images[filename] = item
    print(f". found {len(remote_images)} images")

    missing_local = remote_images.keys() - local_images
    print(f"{missing_local=}")
    for filename in missing_local:
        filepath = os.path.join(repo_folder, filename)
        print("- downloading ..", filepath)
        item = remote_images[filename]
        client.download_image(item.link, filepath)

    missing_remote = local_images - remote_images.keys()
    print(f"{missing_remote=}")
    for filename in missing_remote:
        filepath = os.path.join(repo_folder, filename)

        print("- uploading ..", filepath, end="")
        new_image = client.upload_image(filepath)
        new_filename = os.path.basename(new_image.link)
        new_filepath = os.path.join(repo_folder, new_filename)

        print(f". done, moving {filename} to {new_filename}")
        os.rename(filepath, new_filepath)


if __name__ == "__main__":
    client = ImgurClient()
    sync_user_gallery(client)
