from enum import Enum


class EntityType(Enum):
    Disease = 1
    Species = 2
    Gene = 3
    Chemical = 4
    ProteinMutation = 5
    DNAMutation = 6
    FamilyName = 7
    DomainMotif = 8
    SNP = 9
    OtherNull = 10

    @classmethod
    def from_string(self, input_string):
        string_to_entity = {
            "Disease": self.Disease,
            "Species": self.Species,
            "Gene": self.Gene,
            "Chemical": self.Chemical,
            "ProteinMutation": self.ProteinMutation,
            "DNAMutation": self.DNAMutation,
            "FamilyName": self.FamilyName,
            "DomainMotif": self.DomainMotif,
            "SNP": self.SNP,
            "OtherNull": self.OtherNull
        }

        return string_to_entity.get(input_string, None)
