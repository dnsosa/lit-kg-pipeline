import json

import requests
from requests import HTTPError
import pandas as pd


class Paper:
    """
    A class for storing a single research paper with helpful information retrieval functions
    """

    def __init__(self, item: pd.DataFrame):
        """
        Paper constructor

        :param item: the single-row Pandas dataframe which is at the heart of this representation
        """
        self.paper = item
        #print("Hello")
        #print(self.paper.sha)
        #print(self.paper.sha.values)
        #print(self.paper.sha.values[0])
        #print("Goodbye")

        if len(self.paper.sha.values) != 0:
            self.sha = self.paper.sha.values[0]  # have to unpack value from the Pandas Series class
        else:
            self.sha = None

        if len(self.paper.cord_source.values) != 0:
            self.cord_source = self.paper.cord_source.values[0]
        else:
            self.cord_source = None

        if len(self.paper.doi.values) != 0:
            self.doi = self.paper.doi.values[0]
        else:
            self.doi = None

        if len(self.paper.title.values) != 0:
            self.title = self.paper.title.values[0]
        else:
            self.title = None

        if len(self.paper.abstract.values) != 0:
            self.abstract = self.paper.abstract.values[0]
        else:
            self.abstract = None

        if len(self.paper.authors.values) != 0:
            self.authors = self.paper.authors.values[0]
        else:
            self.authors = None

    @staticmethod
    def get(url, timeout=6):
        """
        Retrieve XML from a URL

        :param url: URL being requested
        :param timeout: time allowed before timeout
        :return: XML text
        """
        try:
            r = requests.get(url, timeout=timeout)
            return r.text
        except ConnectionError:
            print('Cannot connect to {}'.format(url))
        except HTTPError:
            print('Got http error', r.status, r.text)

    @staticmethod
    def format_body(json_file: dict):
        """
        Parse a JSON text into a readable string. Necessary for future text processing

        :param json_file: JSON file to parse
        :return: String representation of the *body* of the JSON with all tags removed and subsections joined together
        """

        # These first four lines are to resolve cases where one section contains multiple subsections of text,
        # so first must group all subsections' text together at the section level
        texts = [(di['section'], di['text']) for di in json_file['body_text']]
        texts_di = {di['section']: "" for di in json_file['body_text']}

        for section, text in texts:
            texts_di[section] += text

        body = ""

        for section, text in texts_di.items():
            body += section
            body += "\n\n"
            body += text
            body += "\n\n"

        return body

    def xml_from_doi(self):
        """
        Load the paper from doi.org and display as text. Requires Internet to be ON

        :return: XML file
        """

        text_xml = self.get(self.doi)
        # text_json = json.dumps(xmltodict.parse(text_xml)) # Attempts at parsing the XML, but failed.
        # formatted_text = self.format_body(text_json)
        return text_xml

    def text_from_file(self):
        """
        Retrieve nicely formatted full text body from the downloaded JSON files

        :return: String representation of the *body* of the JSON with all tags removed and subsections joined together
        """
        version = '2020-03-13'  # Todo: make this not a magic number!
        filename = '../../../data/{}/{}/{}/{}.json'.format(version, self.cord_source, self.cord_source, self.sha)
        f = open(filename, 'r')
        text = json.load(f)  # need to be bytestream???
        f.close()
        formatted_text = self.format_body(text)
        return formatted_text

    def get_author_list(self, split=False):
        """
        Get a list of authors

        :param split: Split author list?
        :return: author list
        """

        authors = self.authors
        if not self.authors:
            return []
        if not split:
            return self.authors
        if self.authors.startswith('['):
            self.authors = authors.lstrip('[').rstrip(']')
            return [a.strip().replace("\'", "") for a in authors.split("\',")]

        # Todo: Handle cases where author names are separated by ","
        return [a.strip() for a in authors.split(';')]

    def get_sha(self):
        return self.sha

    def get_cord_source(self):
        return self.cord_source

    def get_paper(self):
        return self.paper

    def get_doi(self):
        return self.doi

    def get_title(self):
        return self.title

    def get_abstract(self):
        return self.abstract

