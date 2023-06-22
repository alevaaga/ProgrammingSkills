import pandas as pd


class SearchIndex:

    instance = None

    def __init__(self, ):
        self.dataset = None

    @staticmethod
    def get():
        if SearchIndex.instance is None:
            SearchIndex.instance = SearchIndex()
        return SearchIndex.instance

    def configure(self, dataset: pd.DataFrame):
        self.dataset = dataset
