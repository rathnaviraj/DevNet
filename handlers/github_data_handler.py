
from handlers.base_data_handler import BaseDataHandler


class GitHubDataHandler(BaseDataHandler):

    def __init__(self, username, repository=None, token=None, *args, **kwargs):
        self.username = username
        self.repository = repository
        print(repository)
        super().__init__(*args, **kwargs)

    def get_contributors(self):
        contributors_url = f'https://api.github.com/repos/{self.username}/{self.repository}/contributors'
        return self._fetch_data(contributors_url)