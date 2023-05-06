from .utils import filter_items
from duckduckgo_search import ddg

import os
import requests

class BingAPI(object):
    subscription_key = os.getenv('BING_SEARCH_V7_SUBSCRIPTION_KEY')
    endpoint = 'https://api.bing.microsoft.com/v7.0/search'
    keywords = ['name', 'url', 'snippet']

    def request(self, query, max_results):
        response = requests.get(
            self.endpoint
          , headers={'Ocp-Apim-Subscription-Key': self.subscription_key}
          , params={
                'q': query
              , 'mkt': 'en-US'
              , 'count': max_results
              , 'offset':0
            }
        )

        return response

    def search(self, query, max_results=5):
        try:
            response = self.request(query, max_results)
            result = response.json()['webPages']['value']
        except Exception:
            result = []
            raise Exception('Bing endpoint could not be resolved due to a certain error')
        finally:
            return [filter_items(v, self.keywords) for v in result]      

class DuckDuckGOAPI(object):
    keywords = ['title', 'body', 'href']

    def request(self, query, max_results):
        response = ddg(
            query
          , region='wt-wt'
          , safesearch='Moderate'
          , time='y'
          , max_results=max_results
        )

        return response

    def search(self, query, max_results=5):
        try:
            result = self.request(query, max_results)
        except Exception:
            result = []
            raise Exception('DuckDuckGo endpoint could not be resolved due to a certain error')
        finally:
            return [filter_items(v, self.keywords) for v in result]
