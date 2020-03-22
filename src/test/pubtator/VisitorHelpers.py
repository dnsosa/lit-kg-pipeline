from src.main.pubtator.Visitor import Visitor


class RecordCountVisitor(Visitor):
    def __init__(self):
        self.count = 0

    def visit(self, item):
        self.count += 1

    def get_count(self):
        return self.count


class RecordStoreVisitor(Visitor):
    def __init__(self):
        self.records = []

    def visit(self, item):
        self.records.append(item)

    def get_records(self):
        return self.records
