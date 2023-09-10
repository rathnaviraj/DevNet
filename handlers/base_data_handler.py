import requests

class BaseDataHandler:

    def __init__(self, token=None, *args, **kwargs):
        self.token = token

    def _fetch_data(self, url:str):
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_contributors(self):
        return None