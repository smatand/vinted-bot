import os
import requests
from requests.exceptions import HTTPError
import pickle
from settings import VINTED_URL


class VintedRequestSettings:
    HEADERS = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Host": VINTED_URL,
        "Referer": VINTED_URL,
        "Accept-Language": "en-US,en;q=0.5"
    }
    AUTH_URL = f"https://{VINTED_URL}/auth/token_refresh"
    COOKIES_FILE = "cookies.pkl"
    MAX_TRIES = 3


class VintedRequest:
    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(VintedRequestSettings.HEADERS)
        self.obtain_cookies_from_file()

    def obtain_cookies_from_file(
            self,
            file_path=VintedRequestSettings.COOKIES_FILE
            ):
        """Obtains cookies from a file

        Keyword arguments:
        file_path -- path to the file
        """
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                self._session.cookies.update(pickle.load(f))

    def save_cookies_to_file(
            self,
            file_path=VintedRequestSettings.COOKIES_FILE
            ):
        """Stores cookies to a file

        Keyword arguments:
        file_path -- path to the file
        """
        with open(file_path, "wb") as f:
            pickle.dump(self._session.cookies, f)

    def get(self, url):
        """Sends a GET request

        Keyword arguments:
        url -- url to send the request to
        """
        tries = 1
        while tries < VintedRequestSettings.MAX_TRIES:
            tries += 1

            with self._session.get(url) as response:
                if response.status_code == 401:
                    self.refresh_token()
                elif response.status_code == 200:
                    return response
                else:
                    raise HTTPError(
                            "Status code {}".format(response.status_code)
                        )

    def post(self, url):
        """Sends a POST request

        Keyword arguments:
        url -- url to send the request to
        """
        response = self._session.post(url)
        response.raise_for_status()
        return response

    def refresh_token(self):
        """Refreshes the token"""
        self._session.cookies.clear_session_cookies()

        try:
            self.post(VintedRequestSettings.AUTH_URL)
        except HTTPError as e:
            print("Error while refreshing the token: {}".format(e))

        self.save_cookies_to_file()
