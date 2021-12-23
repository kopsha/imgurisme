import configparser
from imgurpython import ImgurClient


def authenticate(use_credentials):
    client = ImgurClient(**use_credentials)

    # Authorization flow, pin example (see docs for other auth types)
    authorization_url = client.get_auth_url('pin')

    print("Go to the following URL: {0}".format(authorization_url))

    # Read in the pin, handle Python 2 or 3 here.
    pin = input("Enter pin code: ")

    # ... redirect user to `authorization_url`, obtain pin (or code or token) ...
    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

    print("   Access token:  {0}".format(credentials['access_token']))
    print("   Refresh token: {0}".format(credentials['refresh_token']))

    print("Authentication successful! Here are the details:")
    with open("auth_cache.ini", "w") as auth_cache:
        config["credentials"]["access_token"] = credentials['access_token']
        config["credentials"]["refresh_token"] = credentials['refresh_token']
        config.write(auth_cache)
        print("saved to cache")

    return client


def example(client):
    """Example request"""
    account = client.get_account("flowRunner")
    print(account.__dict__)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("auth_cache.ini")

    credentials = dict()
    if config.has_section("credentials"):
        print("loaded credentials from cache")
        credentials["client_id"] = config.get("credentials", "client_id")
        credentials["client_secret"] = config.get("credentials", "client_secret")
        credentials["access_token"] = config.get("credentials", "access_token")
        credentials["refresh_token"] = config.get("credentials", "refresh_token")
        client = ImgurClient(**credentials)
    else:
        print("running authentication protocol")
        credentials["client_id"] = '392b2ee98809bcc'
        credentials["client_secret"] = 'a44474275ff43411f1fbb9836637bd600fbfe39a'
        client = authenticate(credentials)

    example(client)
