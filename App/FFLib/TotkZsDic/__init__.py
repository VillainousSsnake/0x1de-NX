import os
import zipfile


class ZsDic:
    @staticmethod
    def get_dict(dict_type: str) -> bytes:
        """
        :param dict_type: type of dictionary to return. Can be 'zs', 'pack', 'bcett', or 'byml'
        :return: bytes or binary data
        """

        # Creating the zip controller
        zip_controller = zipfile.ZipFile(
            os.path.join(
                os.path.dirname(
                    os.path.abspath(
                        __file__
                    )
                ), "ZsDic.zip"
            ), mode='r'
        )

        # Match statement for the dict_type
        match dict_type:

            case 'zs':  # If dict_type is 'zs'
                return zip_controller.read(name='zs.zsdic')

            case 'pack':    # If dict_type is 'pack'
                return zip_controller.read(name='pack.zsdic')

            case 'bcett.byml':  # If dict_type is 'bcett.byml'
                return zip_controller.read(name='bcett.byml.zsdic')

        # If dict_type wasn't a valid value, raise error
        raise ValueError(
            "dict_type param may either be 'zs', 'pack', 'bcett', or 'byml'. It can't be " + dict_type
        )

    @staticmethod
    def detect_zstandard_dict(file_name) -> str | None:
        """
        Automatically detects which dictionary to return when given the file's file name
        :param file_name: The file name of the file
        :return: bytes or None
        """

        if '.pack.zs' in file_name:  # If dict type is 'pack'
            return 'pack'

        elif 'bcett.byml.zs' in file_name:  # If dict type is 'bcett.byml'
            return 'bcett.byml'

        elif '.zs' in file_name:  # If dict type is 'zs'
            return 'zs'

        # Returning None if no dictionary was detected
        return None

    @staticmethod
    def auto_decompress_file(file_path) -> bytes:

        # Creating output variable
        output = bytes()

        # Creating the file name variable
        file_name = os.path.basename(file_path)

        # TODO: Put code here

        # Returning output
        return output
