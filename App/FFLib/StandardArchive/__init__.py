# App/FFLib/StandardArchive/__init__.py
# Contains Sarc class

# Importing modules
from App.FFLib.TotkZsDic import ZsDic
import zstandard
import tempfile
import sarc
import os
import typing


class Sarc:
    @staticmethod
    def list_sarc_contents(
            _input: os.PathLike | bytes | typing.BinaryIO,
            mode: str) -> list:
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

                # Getting the file data and magic
                with open(_input, "rb") as f_in:
                    file_magic = f_in.read(4)

                with open(_input, "rb") as f_in:
                    file_data = f_in.read()

                # Detecting if the file is zstandard
                if file_magic == b"(\xb5/\xfd":
                    file_data = ZsDic.auto_decompress_file(_input)

                # Creating the sarc controller
                sarc_controller = sarc.SARC(file_data)

                # Setting output to the list of files
                output = []

                for key in sarc_controller.list_files().mapping:
                    output.append(key)

            case "d":

                # Creating the sarc controller
                sarc_controller = sarc.SARC(_input)

                # Setting output to the list of files
                output = sarc_controller.list_files()

            case "s":

                # Creating sarc controller with file object
                sarc_controller = sarc.read_file_and_make_sarc(_input)

                # Setting output to the list of files
                output = sarc_controller.list_files()

        return output
