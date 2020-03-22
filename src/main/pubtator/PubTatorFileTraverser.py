from .EntityType import EntityType
from .PubTatorRecord import PubTatorRecord

from io import BytesIO
import re

TITLE_SPLIT_PATTERN = re.compile(b"\\|")
ABSTRACT_LINE_SPLIT_PATTERN = re.compile(b"\\|")
ANNOTATION_LINE_SPLIT_PATTERN = re.compile(b"\t")


class PubTatorFileTraverser:

    def __init__(self, pubtator_input_stream):
        self.input_stream = pubtator_input_stream

    def traverse_rows(self, visitor):

        buffered_reader = BytesIO(self.input_stream)  # Maybe be concerned about bytes...

        while True:
            record = PubTatorRecord()
            title_line = buffered_reader.readline()
            if title_line is None or title_line is b'': #checking both is a hack. What's buffered_reader's behavior if empty string...?
                break
            title_data = TITLE_SPLIT_PATTERN.split(title_line)
            record.set_pmid(int(title_data[0].decode('utf-8')))
            if len(title_data) == 3:
                record.set_title(title_data[2])
            else:
                record.set_title("")

            abstract_line = re.split(ABSTRACT_LINE_SPLIT_PATTERN, buffered_reader.readline())
            if len(abstract_line) == 3:
                record.set_abstract_text(abstract_line[2])
                record.set_text(record.get_title() + b"\n" + record.get_abstract_text())
            else:
                record.set_abstract_text("")
                record.set_text(record.get_title())

            annotation_line = re.split(ANNOTATION_LINE_SPLIT_PATTERN, buffered_reader.readline())
            while len(annotation_line) > 1:
                start = int(annotation_line[1])
                end = int(annotation_line[2])
                record.add_position(start, end)
                record.add_string(annotation_line[3])
                record.set_string_for_position(start, end, annotation_line[3])
                if len(annotation_line) >= 5:
                    e_type = EntityType.from_string(annotation_line[4].decode('utf-8'))
                    record.add_entity_type(e_type)
                    record.set_entity_type_for_position(start, end, e_type)
                else:
                    record.add_entity_type(None)

                if len(annotation_line) == 6:
                    record.set_entity_id_for_position(start, end, annotation_line[5])
                    record.add_entity_id(annotation_line[5])
                else:
                    record.add_entity_id(None)

                # Need a try-except here?
                annotation_line = re.split(ANNOTATION_LINE_SPLIT_PATTERN, buffered_reader.readline())
                if annotation_line is None:
                    break

            visitor.visit(record)
        buffered_reader.close()
