from bots.twitter.auth import initalize_auth


def tweet_image(file_path, status=None):
    api = initalize_auth()
    api.update_with_media(file_path, status)
