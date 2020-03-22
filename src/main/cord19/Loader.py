from pathlib import Path, PurePath
import pandas as pd
import os

from src.main.cord19.PaperSet import PaperSet

biorxiv_dir = '../../../data/2020-03-13/biorxiv_medrxiv/biorxiv_medrxiv/'
comm_dir = '../../../data/2020-03-13/comm_use_subset/comm_use_subset/'
noncomm_dir = '../../../data/2020-03-13/noncomm_use_subset/noncomm_use_subset/'
pmc_dir = '../../../data/2020-03-13/pmc_custom_license/pmc_custom_license/'

biorxiv_files = os.listdir(biorxiv_dir)
comm_files = os.listdir(comm_dir)
noncomm_files = os.listdir(noncomm_dir)
pmc_files = os.listdir(pmc_dir)


class Loader:
    """
    Class for loading files into a PaperSet representation based on the metadata file provided
    """

    def __init__(self, data_dir, metadata_file):
        self.data_dir = PurePath(data_dir)
        self.metadata_file = metadata_file
        self.metadata_path = str(self.data_dir / self.metadata_file)
        self.metadata = None
        self.paper_set = None

        try:
            self.load_metadata()
        except FileNotFoundError as e:
            print("FileNotFoundError: {} could not be found".format(self.metadata_path))

    def load_metadata(self):
        """
        Creates a PaperSet object based on the input data. Loads all full text available.
        """


        metadata = pd.read_csv(self.metadata_path, dtype={'Microsoft Academic Paper ID': str, 'pubmed_id': str})

        def doi2url(d):
            return 'http://{}'.format(d) if d.startswith('doi.org') else 'http://doi.org/{}'.format(d)

        def sha2source(d):
            sha_json = d + ".json"
            if sha_json in biorxiv_files:
                return "biorxiv_medrxiv"
            elif sha_json in comm_files:
                return "comm_use_subset"
            elif sha_json in noncomm_files:
                return "noncomm_use_subset"
            elif sha_json in pmc_files:
                return "pmc_custom_license"
            else:
                return None

        def get_text(sha, paper_set):
            paper = paper_set.get_by_sha(sha)
            if paper.paper.empty:
                return ''

            has_full_text = paper.paper.has_full_text.values[0]
            return paper.text_from_file() if has_full_text else ''

        # Convert doi to url
        metadata.doi = metadata.doi.fillna('').apply(doi2url)

        # Get the source of the paper
        metadata['cord_source'] = metadata.sha.fillna('').apply(sha2source)

        # Get full text from the JSON files downloaded
        metadata['full_text'] = metadata.sha.fillna('').apply(get_text, paper_set=PaperSet(metadata))

        # Set abstract to paper title if it's null
        metadata.abstract = metadata.abstract.fillna(metadata.title)

        # Remove duplicate papers (collected from separate sources)
        # todo: how to handle if paper is collected from multiple sources, make note of multiple sources?

        # duplicate_paper = ~(metadata.title.isnull() | metadata.abstract.isnull()) & \
        #                   (metadata.duplicated(subset=['title', 'abstract']))

        # metadata = metadata[~duplicate_paper].reset_index(drop=True) # should I remove duplicates?

        self.metadata = metadata
        self.paper_set = PaperSet(metadata)

    def get_metadata(self):
        return self.metadata

    def get_paper_set(self):
        return self.paper_set

