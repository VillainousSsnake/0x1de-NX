# App/FFLib/StandardArchive/__init__.py
# Contains Sarc class

# Importing modules
import zstandard
import tempfile
import os
import sarc


class Sarc:
    @staticmethod
    def list_sarc_contents(_input: os.PathLike | bytes, mode="fp") -> list:
        """
        :param _input: Input data (Type depends on the mode)
        :param mode: The mode of the function (Modes explained below)
        :return: list of files

        MODES:
            - 'fp': Interprets _input as a PathLike object
            - 'd': Interprets _input as data
        """

        output = []

        match mode:

            case "fp":
                pass    # TODO: Stub

            case "d":
                pass    # TODO: Stub

        return output
