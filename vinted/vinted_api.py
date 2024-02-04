from settings import VINTED_URL
from request import VintedRequest
import pandas as pd

import re


class VintedApiSettings:
    API_APPEND = "/api/v2"  # www.vinted.sk/api/v2 is the api url
    API_URL = f"https://{VINTED_URL}{API_APPEND}"
    FILTER_PARAMS = [
        "catalog",
        "color_ids",
        "brand_ids",
        "size_ids",
        "material_ids",
        "video_game_rating_ids",
        "status_ids",
    ]
    SINGLE_NUMBER_PARAMS = [
        "price_from",
        "price_to",
    ]
    OTHER_PARAMS = [
        "currency",
        "search_text",
        "order",
    ]
    COLUMNS = [
        "id",
        "title",
        "price",
        "brand_title",
        "title",
        "discount",
        "favourite_count",
        "is_visible",
        "view_count",
        "photo",
        "url",
        "total_item_price"
    ]


class VintedApi:
    def __init__(self):
        # predefine session with headers and cookies
        self._request = VintedRequest()

    def search_url(self, url, per_page=16):
        """Retrieve items from a given url.

        Keyword arguments:
        url -- the url to get the items from

        Returns:
        list -- a list of items or None
        """
        url = self.parse_url(url, per_page=per_page)
        try:
            with self._request.get(url) as response:
                return self.process_dataframe(response.json())

        except Exception as e:
            print("Error while retrieving items: {}".format(e))
            return None

    def process_dataframe(self, response_json):
        """Processes the json into a dataframe

        Keyword arguments:
        json -- the json to process

        Returns:
        dataframe -- the processed dataframe
        """
        df = pd.DataFrame(response_json["items"])

        df = df.reindex(
            columns=VintedApiSettings.COLUMNS
        )

        df["favourite_count"] = df["favourite_count"].astype(int)
        # as items['photo'] is a list of dicts, we need just the 1st 'url'
        df['photo_url'] = df['photo'].apply(lambda x: x['url'])
        # drop the 'photo' column
        df.drop(columns=['photo'], inplace=True)

        return df

    def parse_url(self, url, page=1, per_page=16):
        """Parses vinted.sk/.. to api form of url

        Keyword arguments:
        url -- the url to parse

        Returns:
        url with parameters of search
        """
        api_url = f"{VintedApiSettings.API_URL}/catalog/items?page={page}&per_page={per_page}"

        for param in VintedApiSettings.FILTER_PARAMS:
            api_url += VintedApi.add_filter_param_to_url(url, param)

        for param in VintedApiSettings.SINGLE_NUMBER_PARAMS:
            param_value = re.findall(fr"{param}=(\d+)", url)

            if param_value:
                # if there are more than one param, take the first one
                # "to_price=30&to_price=40" -> "to_price=30"
                api_url += f"&{param}={param_value[0]}"

        for param in VintedApiSettings.OTHER_PARAMS:
            param_value = re.findall(fr"{param}=([^&]+)", url)

            if param_value:
                # take the 1st param again
                api_url += f"&{param}={param_value[0]}"

        return api_url

    def add_filter_param_to_url(url, param_name):
        """Adds filter param to the url
        f. e. "color_ids[]=1&color_ids[]=2&color_ids[]=3"

        Keyword arguments:
        url -- the url with the param to parse
        param_name -- the name of the param to parse

        Returns:
        string -- the string in format "&color_ids=1,2,3"
        """

        params = ""
        param_ids = re.findall(fr"{param_name}\[\]=(\d+)", url)
        if param_ids:
            # specific case, where catalog is not catalog_ids
            if param_name == 'catalog':
                params += f"&catalog_ids={','.join(param_ids)}"
            else:
                params += f"&{param_name}={','.join(param_ids)}"

        return params
