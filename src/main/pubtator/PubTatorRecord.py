from .EntityType import EntityType


class PubTatorRecord:

    def __init__(self):
        self.pmid = None
        self.title = None
        self.abstract_text = None
        self.text = None
        self.positions = []
        self.strings = []
        self.entity_types = []
        self.entity_ids = []
        self.position_to_string_map = {}
        self.position_to_entity_type = {}
        self.position_to_entity_id = {}

    def get_pmid(self):
        return self.pmid

    def set_pmid(self, pmid):
        self.pmid = pmid

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_abstract_text(self):
        return self.abstract_text

    def set_abstract_text(self, abstract_text):
        self.abstract_text = abstract_text

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text

    def add_position(self, start, end):
        self.positions.append((start, end))

    def add_string(self, string):
        self.strings.append(string)

    def add_entity_type(self, entity_type):
        self.entity_types.append(entity_type)

    def add_entity_id(self, entity_id):
        self.entity_ids.append(entity_id)

    def get_entity_ids(self):
        return self.entity_ids

    def get_strings(self):
        return self.strings

    def get_positions(self):
        return self.positions

    def get_sorted_positions(self):
        # Sort by start position is default behavior
        sorted_positions = sorted(self.positions)
        return sorted_positions

    def get_string_for_position(self, start, end):
        return self.position_to_string_map.get((start, end), None)

    def get_entity_type_for_position(self, start, end):
        return self.position_to_entity_type.get((start, end), EntityType.OtherNull)

    def get_entity_id_for_position(self, start, end):
        return self.position_to_entity_id.get((start, end), None)

    def set_string_for_position(self, start, end, string):
        self.position_to_string_map[(start, end)] = string

    def set_entity_type_for_position(self, start, end, e_type):
        self.position_to_entity_type[(start, end)] = e_type

    def set_entity_id_for_position(self, start, end, e_id):
        self.position_to_entity_id[(start, end)] = e_id

    def __str__(self):
        string_rep = "PubTatorRecord{" + \
                     "pmid='" + self.pmid + '\'' + \
                     ", title='" + self.title + '\'' + \
                     ", abstractText='" + self.abstract_text + '\'' + \
                     ", text='" + self.text + '\'' + \
                     ", positions=" + str(self.positions) + \
                     ", strings=" + str(self.strings) + \
                     ", entityTypes=" + str(self.entity_types) + \
                     ", entityIds=" + str(self.entity_ids) + \
                     '}'

        return string_rep
