# App/FFLib/StandardArchive/__init__.py
# Contains Sarc class

# Importing modules
import zstandard
import tempfile
import sarc
import os
import typing


class Sarc:
    @staticmethod
    def list_sarc_contents(_input: os.PathLike | bytes | typing.BinaryIO, mode="fp") -> list:
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

                # Creating sarc controller
                with open(_input, "rb") as f_in:
                    sarc_controller = sarc.read_file_and_make_sarc(f_in)

                # Setting output to the list of files
                output = sarc_controller.list_files()

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
