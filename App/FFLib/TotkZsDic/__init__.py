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

            case 'bcett':   # If dict_type is 'bcett'
                return zip_controller.read(name='bcett.byml.zsdic')

            case 'byml':    # If dict_type is 'byml'
                return zip_controller.read(name='bcett.byml.zsdic')

        # If dict_type wasn't a valid value, raise error
        raise ValueError(
            "dict_type param may either be 'zs', 'pack', 'bcett', or 'byml'. It can't be " + dict_type
        )
