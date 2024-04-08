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
    def compress_sarc_from_dir(input_dir: os.PathLike | str) -> bytes:
        """
        Compresses the given input directory, compresses it as a
        sarc archive, and returns the compressed sarc archive data

        :param input_dir: Input path for the directory to compress
        :return: compressed sarc archive data (bytes)
        """

        pass    # TODO: Stub

    @staticmethod
    def extract_sarc_to_dir(
            _input: os.PathLike | bytes | typing.BinaryIO,
            out_dir: os.PathLike | str,
            mode: str = "fp",) -> None:
        """
        Extracts sarc files and folders to a directory

        :param _input: Input path/bytes/stream (Type depends on the mode)
        :param out_dir: The path to extract the input SARC files
        :param mode: The mode of the function (Modes explained below)
        :return: None

        MODES:
            - 'fp': Interprets _input as a PathLike object
            - 'd': Interprets _input as data
            - 's': Interprets _input as a file stream
        """

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

                # Extracting the files
                sarc_controller.extract_to_dir(out_dir)

            case "d":

                # Creating the sarc controller
                sarc_controller = sarc.SARC(_input)

                # Extracting the files
                sarc_controller.extract_to_dir(out_dir)

            case "s":

                # Creating sarc controller with file object
                sarc_controller = sarc.read_file_and_make_sarc(_input)

                # Extracting the files
                sarc_controller.extract_to_dir(out_dir)

        return None

    @staticmethod
    def list_sarc_contents(
            _input: os.PathLike | bytes | typing.BinaryIO,
            mode: str) -> list:
        """
        Returns a list of sarc file paths from within a sarc

        :param _input: Input path/bytes/stream (Type depends on the mode)
        :param mode: The mode of the function (Modes explained below)
        :return: list of files

        MODES:
            - 'fp': Interprets _input as a PathLike object
            - 'd': Interprets _input as data
            - 's': Interprets _input as a file stream
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
