"""Lets see what dictionaries have to say"""

import  requests
from immutable_objects import ImmutableData


class OxfordDictionary:

    API_BASE = "https://od-api.oxforddictionaries.com/api/v2"
    LANGUAGE = 'en-gb'

    def __init__(self):
        self.headers = dict(
            app_id="2be63691",
            app_key="7bac385b2701d50df4b089bded547994",
        )

    def api_get(self, api):
        url = f"{self.API_BASE}/{api}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        data = ImmutableData(response.json())
        return data

    def entries(self, word):
        api_url = f"entries/{self.LANGUAGE}/{word.lower()}"
        return self.api_get(api_url)

    def lemmas(self, word):
        api_url = f"lemmas/{self.LANGUAGE}/{word.lower()}"
        return self.api_get(api_url)


def main():
    oxd = OxfordDictionary()
    data = oxd.entries("keyboard")
    print(f"{data=}")

    data = oxd.lemmas("runner")
    print(f"{data=}")


if __name__ == "__main__":
    main()
