import os
import pandas as pd
import csv
import json
import re
from pprint import pprint

# Standard Header Format for MI-TAB 2.7
mitab_header = [
    'Unique identifier for interactor A',
    'Unique identifier for interactor B',
    'Alternative identifier for interactor A',
    'Alternative identifier for interactor B',
    'Aliases for A',
    'Aliases for B',
    'Interaction detection methods',
    'First author',
    'Identifier of the publication',
    'NCBI Taxonomy identifier for interactor A',
    'NCBI Taxonomy identifier for interactor B',
    'Interaction types',
    'Source databases',
    'Interaction identifiers',
    'Confidence score',
    'Complex expansion',
    'Biological role A',
    'Biological role B',
    'Experimental role A',
    'Experimental role B',
    'Interactor type A',
    'Interactor type B',
    'Xref for interactor A',
    'Xref for interactor B',
    'Xref for the interaction',
    'Annotations for interactor A',
    'Annotations for Interactor B',
    'Annotations for the interaction',
    'NCBI Taxonomy identifier for the host organism',
    'Parameters of the interaction',
    'Creation date',
    'Update date',
    'Checksum for interactor A',
    'Checksum for interactor B',
    'Checksum for interaction',
    'negative',
    'Features for interactor A',
    'Features for interactor B',
    'Stoichiometry for interactor A',
    'Stoichiometry for interactor B',
    'Participant identification method for interactor A',
    'Participant identification method for interactor B']

# Sherlock format
sherlock_keys = [
    "interactor_a_id",
    "interactor_b_id",
    "interactor_a_id_type",
    "interactor_b_id_type",
    "interactor_b_tax_id",
    "interactor_a_molecula_type_mi_id",
    "interactor_b_molecula_type_mi_id",
    "interactor_a_molecula_type_name",
    "interactor_b_molecula_type_name",
    "interaction_detection_methods_mi_id",
    "interaction_types_mi_id",
    "source_databases_mi_id",
    "pmids"
]


class MiTabHandler:

    """
    A class for handling the defined data structure for the Navi-MiTab Structure. It
    does this through the use of Pandas Dataframe which holds the tabular format. The
    Sherlock structure is read in line by line without be held in memory and then added
    to the Navi-MiTab dataframe. This dataframe can the be serialise out with or without
    a header. Regex is used to validate the inputs and outputs for the sherlock file
    and IDs can be mapped using the id-mapper module.

    The dataframe uses the MiTab 2.7 format;

    """

    def __init__(self):
        # Create a map for each format
        self._map_mitab()
        self._map_sherlock()
        self.network = pd.DataFrame(columns=mitab_header)

    def _map_mitab(self):
        """ MiTab 2.7 identifiers """
        (self.uidA, self.uidB, self.altA, self.altB, self.aliasA,
         self.aliasB, self.method, self.authors, self.pmids,
         self.taxA, self.taxB, self.interactionType, self.sourcedb,
         self.interactionIdentifiers, self.confidence, self.complex,
         self.bioRoleA, self.bioRoleB, self.experRoleA, self.experRoleB,
         self.interTypeA, self.interTypeB, self.xrefA, self.xrefB,
         self.xrefIneraction, self.annotA, self.annotB, self.annotInter,
         self.hostOrganism, self.interactionParams, self.creationData, self.updateDate,
         self.checkSumA, self.checkSumB, self.checkSumInter, self.negative,
         self.featureInterA, self.featureInterB, self.stoichiometryA,
         self.stoichiometryB, self.partInterA, self.partInterB) = mitab_header[:42]

    def _map_sherlock(self):
        """ Sherlock identifiers """
        self.sher_a_id = sherlock_keys[0]
        self.sher_b_id = sherlock_keys[1]
        self.sher_a_id_type = sherlock_keys[2]
        self.sher_b_id_type = sherlock_keys[3]
        self.sher_b_tax_id = sherlock_keys[4]
        self.sher_a_mol_id = sherlock_keys[5]
        self.sher_b_mol_id = sherlock_keys[6]
        self.sher_a_mol_type = sherlock_keys[7]
        self.sher_b_mol_type = sherlock_keys[8]
        self.sher_methods_mi_id = sherlock_keys[9]
        self.sher_types_mi_id = sherlock_keys[10]
        self.sher_db_mi_id = sherlock_keys[11]
        self.sher_pmids = sherlock_keys[12]

    def add_interaction(self, interaction):
        """ Create a new interaction (row) to add to the network dataframe """
        self.network = self.network.append(interaction, ignore_index=True)

    def parse(self, file_path, file_format='mitab'):
        """
        Main parsing method which directs to the correct format depending on file_format

        Parameters
        ----------
        file_path: str, path to input file to be parsed
        file_format: str, the file format of the file regardless of the file extension

        Returns
        -------
        network: pandas dataframe, optional and should only be used if manipulation or
            duplication of the network is required
        """

        if self._check_file(file_path):
            return

        if file_format == 'sherlock':
            self.network = self.parse_sherlock(file_path)
        elif file_format == 'mitab':
            self.network = self.parse_mitab(file_path)
        else:
            raise IncorrectFileType()

        return self.network

    def parse_mitab(self, file_path):
        """
        Parse the network to pandas dataframe in mitab format

        Parameters
        ----------
        file_path: str, location to file holding the network in mitab format

        Returns
        -------
        network: pandas dataframe, optional and should only be used if manipulation or
            duplication of the network is required
        """

        self.network = pd.read_csv(file_path, delimiter='\t', names=mitab_header)
        self.validate()

        return self.network

    def serialise_mitab(self, file_path, add_header=False):
        """
        Serialise network to mitab format

        Parameters
        ----------
        file_path: str, path and name of the file to write too
        add_header: boolean, if the file should add the mitab header information
        """

        self.validate()
        self.network.to_csv(file_path, sep='\t', index=False, header=add_header)

    def validate(self):
        """
        A function to check the format follows the correct vocab. Ensure that any missing data
        is filled with a "-" to represent a NaN value and that duplicates are removed from the
        dataframe. All values are converted to lowercase.

        Returns
        -------
        Boolean Value of whether the dataframe is valid or not

        """
        try:
            self.network = self.network.fillna('-')
            self.network = self.network.apply(lambda x: x.astype(str).str.lower())
            self.network = self.network.drop_duplicates([mitab_header[0], mitab_header[1]])
            return True
        except Warning:
            return False

    def parse_sherlock(self, file_path):
        """
        Read in Sherlock-json file format and parse it to the internal dataframe used for
        the Navi-MiTAB file structure

        Parameters
        ----------
        file_path, path to the sherlock json file to be parsed to Navi-MiTab format

        Return
        ------
        network, this return is optional, as the instance of the network is saved
        """

        sherlock_network = self._parse_sherlock_structure(file_path)
        inner_structure = {}

        for idx, inter in enumerate(sherlock_network):

            # Create complex string formats
            ref_id = "pudmed"
            prefix = "psi-mi:"
            interactor_a = f"{inter[self.sher_a_id_type]}:{inter[self.sher_a_id]}"
            interactor_b = f"{inter[self.sher_b_id_type]}:{inter[self.sher_b_id]}"
            interactors_ref = "".join([f"{ref_id}:{i};" for i in inter[self.sher_pmids]])
            database_sources = "".join([f"{prefix}\"mi:{source}\"(unknown)|" for source in inter[self.sher_db_mi_id]])
            methods = "".join([f"{prefix}{method}(unknown)|" for method in inter[self.sher_methods_mi_id]])
            inter_types = "".join([f"{prefix}'{types}'(unknown)|" for types in inter[self.sher_types_mi_id]])

            # Create new interaction
            new_row = self.new_interaction()
            new_row[self.uidA] = interactor_a
            new_row[self.uidB] = interactor_b
            new_row[self.taxB] = f"taxid:{inter[self.sher_b_tax_id]} ('homo sapiens')"
            new_row[self.annotA] = f"start:{inter[self.sher_a_mol_type]};{interactor_a.replace(':', ';')}"
            new_row[self.annotB] = f"end:{inter[self.sher_b_mol_type]};{interactor_b.replace(':', ';')}"
            new_row[self.sourcedb] = database_sources[:-1]
            new_row[self.pmids] = interactors_ref[:-1]
            new_row[self.method] = methods[:-1]
            new_row[self.interactionType] = inter_types[:-1]
            new_row[self.interTypeA] = f"{prefix}'mi:{inter[self.sher_a_mol_id]}'(unknown)"
            new_row[self.interTypeB] = f"{prefix}'mi:{inter[self.sher_b_mol_id]}'(unknown)"
            inner_structure[idx] = inter

        self.add_interaction(inner_structure)

        # REMAP MI VOCAB TO MITAB STRING BASED IDS #
        # TODO : Add MI Mapping using the ID mapper module

        self.validate()

        return self.network

    def serialise_sherlock(self, filename):
        """
        Serialise the mitab dataframe to the sherlock format. This only takes in the file path
        and is activated by the a parameter given to the parse method by the user. This is an
        optional parser.

        Parameters
        ----------
        filename: str, path to the output file

        """

        # REMAP THE FILE TO HAVE MI-BASED IDs #
        # TODO : Add MI Mapping using the ID mapper module

        json_objects = []

        for _, row in self.network.iterrows():
            new_row = {}

            # extract information
            uid_a = self._extract_columns(row[self.uidA])
            uid_b = self._extract_columns(row[self.uidB])

            # write to sherlock format
            new_row[self.sher_a_id] = uid_a[1]
            new_row[self.sher_b_id] = uid_b[1]
            new_row[self.sher_a_id_type] = uid_a[0]
            new_row[self.sher_b_id_type] = uid_b[0]
            new_row[self.sher_b_tax_id] = self._extract_single_id(row[self.taxB])
            new_row[self.sher_a_mol_id] = self._extract_single_id(row[self.interTypeA])
            new_row[self.sher_b_mol_id] = self._extract_single_id(row[self.interTypeB])
            new_row[self.sher_a_mol_type] = self._extract_types(row[self.annotA])
            new_row[self.sher_b_mol_type] = self._extract_types(row[self.annotB])
            new_row[self.sher_methods_mi_id] = self._extract_id(row[self.method])
            new_row[self.sher_types_mi_id] = self._extract_id(row[self.interactionType])
            new_row[self.sher_db_mi_id] = self._extract_id(row[self.sourcedb])
            new_row[self.sher_pmids] = self._extract_id(row[self.pmids])
            json_objects.append(new_row)

        with open(filename, mode="w") as f:
            for jsonobj in json_objects:
                jsonstr = json.dumps(jsonobj)
                f.write(jsonstr + "\n")
            f.flush()

    def build_network_frame(self, inner_structure):
        self.network = pd.DataFrame.from_dict(inner_structure, orient='index')

    @staticmethod
    def new_interaction():
        interaction = dict.fromkeys(mitab_header)
        return interaction

    @staticmethod
    def _check_file(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError("Output not found...")

    @staticmethod
    def _check_header(file_path):
        with open(file_path, 'r') as file:
            sniffer = csv.Sniffer()
            has_header = sniffer.has_header(file.read(1024))
            file.seek(0)

            if has_header:
                return True
            else:
                return False

    @staticmethod
    def _parse_sherlock_structure(file):
        for line in open(file, mode='r'):
            yield json.loads(line)

    @staticmethod
    def _extract_columns(row):
        return re.findall(r"[\w']+", row)

    @staticmethod
    def _extract_id(row):
        return list(map(int, re.findall(r"([0-9]+)", row)))

    @staticmethod
    def _extract_single_id(row):
        return int(re.search(r"([0-9]+)", row).group())

    @staticmethod
    def _extract_types(row):
        return re.search(r"\:(.*?)\;", row).group(1)

    def __repr__(self):
        pprint(self.network)

    def __getitem__(self, key):
        try:
            return self.network[key]
        except IndexError:
            raise IndexError


# CLASS ERRORS
class MiTabError(Exception):
    pass


class IncorrectFileType(Exception):
    pass
