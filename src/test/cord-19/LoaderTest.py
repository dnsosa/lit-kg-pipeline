import unittest


from src.main.cord19.Loader import Loader


class LoaderTest(unittest.TestCase):

    def setUp(self):

        self.data_dir = '../../../data/2020-03-13'
        self.metadata_file = 'all_sources_metadata_2020-03-13.csv'

        self.test_sha = '4a077b9696d19b7d7fa3e71560b7fd5f414a4d19'


        #self.paper_text_xml = '<!DOCTYPE html>\n<html lang="en" class="no-js">\n<head>\n    <meta charset="UTF-8"/>\n    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <meta name="access" content="Yes">\n    \n\n    <meta name="journal_id" content="134"/>\n\n    <meta name="dc.title" content="Angiotensin-converting enzyme 2 (ACE2) as a SARS-CoV-2 receptor: molecular mechanisms and potential therapeutic target"/>\n\n    <meta name="dc.source" content="Intensive Care Medicine 2020"/>\n\n    <meta name="dc.format" content="text/html"/>\n\n    <meta name="dc.publisher" content="Springer"/>\n\n    <meta name="dc.date" content="2020-03-03"/>\n\n    <meta name="dc.type" content="BriefCommunication"/>\n\n    <meta name="dc.language" content="En"/>\n\n    <meta name="dc.copyright" content="2020 The Author(s)"/>\n\n    <meta name="dc.rightsAgent" content="journalpermissions@springernature.com"/>\n\n    <meta name="dc.description" content=""/>\n\n    <meta name="prism.iss'
        #self.paper_text_ans = 'Early January 2020, a novel coronavirus (2019-nCoV) was identified as the infectious agent causing an outbreak of viral pneumonia in Wuhan, China, where the first cases had their symptom onset in December 2019 [1] . This newly discovered virus, which causes severe acute respiratory disease, is related to the severe acute respiratory syndrome (SARS) coronavirus and Middle East respiratory syndrome (MERS) coronavirus, but distinct from each of these [2] . The key epidemiological parameters, including incubation period, for this new virus are therefore rapidly being studied from incoming case reports as the epidemic continues. Chief among these key parameters is the incubation period distribution. The range of the values for the incubation period is essential to epidemiological case definitions, and is required to determine the appropriate duration of quarantine. Moreover, knowledge of the incubation period helps to assess the effectiveness of entry screening and contact tracing. The di'

        self.test_paper_xml_1000 = '\n<!DOCTYPE html>\n<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->\n<!--[if IE 7]> <html class="no-js lt-ie9 lt-ie8"> <![endif]-->\n<!--[if IE 8]> <html class="no-js lt-ie9"> <![endif]-->\n<!--[if gt IE 8]><!-->\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" class="no-js"> <!--<![endif]-->\n<head>\n<meta charset="utf-8" />\n<meta http-equiv="X-UA-Compatible" content="IE=Edge" />\n<!-- <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> -->\n<meta name="viewport" content="width=device-width, initial-scale=1" />\n<title>Eurosurveillance | Incubation period of 2019 novel coronavirus (2019-nCoV) infections among travellers from Wuhan, China, 20–28 January 2020</title>\n<link rel="schema.CRAWLER" href="http://labs.ingenta.com/2006/06/16/crawler" />\n<meta name="dc.title" content="Incubation period of 2019 novel coronavirus (2019-nCoV) infections among travellers from Wuhan, China, 20–28 January 2020" />\n<meta name="dc.publisher" content="Eur'
        self.test_paper_text_1000 = '\n\nEarly January 2020, a novel coronavirus (2019-nCoV) was identified as the infectious agent causing an outbreak of viral pneumonia in Wuhan, China, where the first cases had their symptom onset in December 2019 [1] . This newly discovered virus, which causes severe acute respiratory disease, is related to the severe acute respiratory syndrome (SARS) coronavirus and Middle East respiratory syndrome (MERS) coronavirus, but distinct from each of these [2] . The key epidemiological parameters, including incubation period, for this new virus are therefore rapidly being studied from incoming case reports as the epidemic continues. Chief among these key parameters is the incubation period distribution. The range of the values for the incubation period is essential to epidemiological case definitions, and is required to determine the appropriate duration of quarantine. Moreover, knowledge of the incubation period helps to assess the effectiveness of entry screening and contact tracing. The di'

    def test_loader1(self):

        loader = Loader(self.data_dir, self.metadata_file)
        paper_set = loader.get_paper_set()
        metadata = loader.get_metadata()

        self.assertEqual(len(metadata), 25133)
        self.assertEqual(len(paper_set), 25133)
        #print(paper_set.get_by_sha(self.test_sha).xml_from_doi()[:100])
        self.assertEqual(paper_set.get_by_sha(self.test_sha).xml_from_doi()[:1000], self.test_paper_xml_1000)

        #print(paper_set.get_by_sha(self.test_sha).text_from_file()[:100])
        self.assertEqual(paper_set.get_by_sha(self.test_sha).text_from_file()[:1000], self.test_paper_text_1000)


if __name__ == '__main__':
    unittest.main()
