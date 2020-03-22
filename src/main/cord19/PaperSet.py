import pandas as pd

from src.main.cord19.Paper import Paper


class PaperSet:
    """
    A class representation for maintaining a set of papers, the core of which being a Pandas dataframe
    """

    def __init__(self, metadata: pd.DataFrame):
        """
        Construct a set of papers based on a metadata file provided (e.g. from the CORD-19 dataset)
        :param metadata: Pandas dataframe metadata file about the set of papers
        """
        self.metadata = metadata

    def __getitem__(self, item):
        return Paper(self.metadata.iloc[[item]])

    def __len__(self):
        return len(self.metadata)

    def head(self, n):
        return PaperSet(self.metadata.head(n).copy().reset_index(drop=True))

    def tail(self, n):
        return PaperSet(self.metadata.tail(n).copy().reset_index(drop=True))

    def abstracts(self):
        return self.metadata.abstract.dropna()

    def titles(self):
        return self.metadata.title.dropna()

    def get_by_sha(self, sha):
        return Paper(self.metadata[self.metadata['sha'] == sha])

