import os
import json

os.chdir('/Users/dnsosa/Desktop/AltmanLab/SemMedDB/pubtator-nlp-py/src/main/cord19')

from src.main.cord19.Loader import Loader
from src.main.cord19.Paper import Paper
from src.main.cord19.PaperSet import PaperSet

data_dir = '../../../data/2020-03-13'
metadata_file = 'all_sources_metadata_2020-03-13.csv'

test_sha = '4a077b9696d19b7d7fa3e71560b7fd5f414a4d19'
test_paper_xml_1000 = '\n<!DOCTYPE html>\n<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->\n<!--[if IE 7]> <html class="no-js lt-ie9 lt-ie8"> <![endif]-->\n<!--[if IE 8]> <html class="no-js lt-ie9"> <![endif]-->\n<!--[if gt IE 8]><!-->\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" class="no-js"> <!--<![endif]-->\n<head>\n<meta charset="utf-8" />\n<meta http-equiv="X-UA-Compatible" content="IE=Edge" />\n<!-- <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> -->\n<meta name="viewport" content="width=device-width, initial-scale=1" />\n<title>Eurosurveillance | Incubation period of 2019 novel coronavirus (2019-nCoV) infections among travellers from Wuhan, China, 20–28 January 2020</title>\n<link rel="schema.CRAWLER" href="http://labs.ingenta.com/2006/06/16/crawler" />\n<meta name="dc.title" content="Incubation period of 2019 novel coronavirus (2019-nCoV) infections among travellers from Wuhan, China, 20–28 January 2020" />\n<meta name="dc.publisher" content="Eur'
test_paper_text_1000 = 'Early January 2020, a novel coronavirus (2019-nCoV) was identified as the infectious agent causing an outbreak of viral pneumonia in Wuhan, China, where the first cases had their symptom onset in December 2019 [1] . This newly discovered virus, which causes severe acute respiratory disease, is related to the severe acute respiratory syndrome (SARS) coronavirus and Middle East respiratory syndrome (MERS) coronavirus, but distinct from each of these [2] . The key epidemiological parameters, including incubation period, for this new virus are therefore rapidly being studied from incoming case reports as the epidemic continues. Chief among these key parameters is the incubation period distribution. The range of the values for the incubation period is essential to epidemiological case definitions, and is required to determine the appropriate duration of quarantine. Moreover, knowledge of the incubation period helps to assess the effectiveness of entry screening and contact tracing. The di'

loader = Loader(data_dir, metadata_file)
paper_set = loader.get_paper_set()
metadata = loader.get_metadata()

print(paper_set.get_by_sha(test_sha).text_from_file()[:1000])
print(paper_set.get_by_sha(test_sha).xml_from_doi()[:1000])


def get_text(sha, paper_set):
    paper = paper_set.get_by_sha(sha)
    if paper.paper.empty: # check if dataframe is empty
        return ''

    has_full_text = paper.paper.has_full_text.values[0]
    if has_full_text:
        return paper.text_from_file()
    else:
        return ''


metadata.sha.fillna('').apply(get_text, paper_set=PaperSet(metadata))

pape = Paper(metadata[metadata['sha'] == test_sha])
#print(paper_set[0].text_from_file())




biorxiv_dir = '/Users/dnsosa/Desktop/AltmanLab/SemMedDB/pubtator-nlp-py/data/2020-03-13/biorxiv_medrxiv/biorxiv_medrxiv/'
filenames = os.listdir(biorxiv_dir)
print("Number of articles retrieved from biorxiv:", len(filenames))

all_files = []

for filename in filenames:
    filename = biorxiv_dir + filename
    file = json.load(open(filename, 'r')) #open as bitestring....?
    all_files.append(file)