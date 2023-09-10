
from handlers.base_data_handler import BaseDataHandler
from handlers.github_data_handler import GitHubDataHandler


class DataHandlerFactory:

    DATA_HANDLERS = {
        'github': GitHubDataHandler
    }

    def get_data_handler(name) -> BaseDataHandler:
        return DataHandlerFactory.DATA_HANDLERS.get(name)
