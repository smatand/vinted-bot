from request import VintedRequest


class VintedApi:
    def __init__(self):
        # predefine session with headers and cookies
        self._request = VintedRequest()

    def search_url(self, url):
        """Retrieve items from a given url.

        Keyword arguments:
        url -- the url to get the items from

        Returns:
        list -- a list of items or None
        """
        try:
            with self._request.get(url) as response:
                return response.json()["items"]
        except Exception as e:
            print("Error while retrieving items: {}".format(e))
            return None
