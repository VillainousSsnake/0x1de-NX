"""
This is the class for the file formats that are SArc archives (.pack)
"""


from sarc import sarc


class SARC:
    @staticmethod
    def decompress():
        # TODO: Stub
        pass

    @staticmethod
    def compress():
        # TODO: Stub
        pass

    @staticmethod
    def read_file(input_file_path, mode):

        if mode == 'l':

            output = []

            with open(input_file_path, 'rb') as file_in:
                sarc_archive = sarc.read_file_and_make_sarc(file_in)

            if sarc_archive:
                for file_name in sarc_archive.list_files():
                    output.append(file_name)

    @staticmethod
    def read_data(input_data, mode):

        if mode == 'l':

            sarcController = sarc.SARC(input_data)

            return sarcController.list_files()
