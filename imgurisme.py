import os
import random
import re

import chatty_patty
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
    images = client.list_images()
    for image in images:
        filename = os.path.basename(image.link)
        remote_images[filename] = image
    print(f". found {len(remote_images)} images")

    missing_local = remote_images.keys() - local_images
    # print(f"{missing_local=}")
    for filename in missing_local:
        filepath = os.path.join(repo_folder, filename)
        print("- downloading ..", filepath)
        item = remote_images[filename]
        client.download_image(item.link, filepath)

    missing_remote = local_images - remote_images.keys()
    # print(f"{missing_remote=}")
    for filename in missing_remote:
        filepath = os.path.join(repo_folder, filename)

        print("- uploading ..", filepath, end="")
        new_image = client.upload_image(filepath)
        new_filename = os.path.basename(new_image.link)
        new_filepath = os.path.join(repo_folder, new_filename)

        print(f". done, moving {filename} to {new_filename}")
        os.rename(filepath, new_filepath)

    if missing_remote:
        images = client.list_images()

    posts = {post.id: post for post in client.list_posts()}
    # remote_images = {img.id: img for img in client.list_images() if img.id not in posts}
    unpublished_images = [img.id for img in client.list_images() if img.id not in posts]

    if unpublished_images:
        # pick a single image and publish it
        lucky_id = random.choice(unpublished_images)
        lucky_title = chatty_patty.make_headline()
        description = " ".join(
            [
                chatty_patty.make_sentence(),
                chatty_patty.make_sentence(),
                chatty_patty.make_sentence(),
                "Faking it real hard, hopefully we actually make it someday and",
                chatty_patty.make_promise() + ".",
            ]
        )
        client.update_image(lucky_id, lucky_title, description)
        client.share_image(lucky_id, lucky_title, description, tags=["fuckit,nothingmatters"])
        print(f"- created a new post {lucky_title} ({lucky_id})")
        print(f"> {description}")


if __name__ == "__main__":
    chatty_patty.load_all_words()
    client = ImgurClient()
    sync_user_gallery(client)
