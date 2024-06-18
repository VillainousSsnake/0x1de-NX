# App/FFLib/StandardArchive/__init__.py
# Contains Sarc class

# Importing modules
from App.FFLib.TotkZsDic import ZsDic
import subprocess
import zstandard
import typing
import sarc
import os


class Sarc:
    @staticmethod
    def get_sarc_extension_from_file_name(file_name) -> str | None:
        """
        Returns the detected SARC format extension based on the file name.
        :param file_name: The input file name.
        :return: A valid SARC format extension or None
        """
        
        # Detecting zstandard compression
        if ".zs" in file_name:
            
            # Detecting SARC format
            if ".bfarc" in file_name:
                return ".bfarc.zs"
            elif ".bkres" in file_name:
                return ".bkres.zs"
            elif ".blarc" in file_name:
                return ".blarc.zs"
            elif ".genvb" in file_name:
                return ".genvb.zs"
            elif ".pack" in file_name:
                return ".pack.zs"
            elif ".sarc" in file_name:
                return ".sarc.zs"
            elif ".ta" in file_name:
                return ".ta.zs"

        # Detecting SARC format
        elif ".bfarc" in file_name:
            return ".bfarc"
        elif ".bkres" in file_name:
            return ".bkres"
        elif ".blarc" in file_name:
            return ".blarc"
        elif ".genvb" in file_name:
            return ".genvb"
        elif ".pack" in file_name:
            return ".pack"
        elif ".sarc" in file_name:
            return ".sarc"
        elif ".ta" in file_name:
            return ".ta"

        # Returning None
        # (Because it doesn't detect a valid SARC format)
        return None

    @staticmethod
    def compress_sarc_from_dir(input_dir: os.PathLike | str,
                               compress_with_zstd: bool = False) -> bytes:
        """
        Compresses the given input directory, compresses it as a
        SARC archive, and returns the compressed SARC archive data.

        :param input_dir: Input path for the directory to compress
        :param compress_with_zstd: Compresses the output with zstandard algorithm before returning data
        :return: compressed SARC archive data (bytes)
        """

        # Running the command to compress the SARC into a file
        subprocess.run(
            os.path.join(os.getcwd(), "App", "Bin", "sarc_tool", "sarc_tool.exe")
            + " main -little " + input_dir.replace("/", "\\")
        )

        # Reading the file data
        with open(input_dir + ".sarc", "rb") as f_in:
            file_data = f_in.read()

        # Removing the file
        os.remove(input_dir + ".sarc")

        # Compressing with zstandard compression algorithm
        if compress_with_zstd:

            # Getting the compression dictionary type
            dict_type = ZsDic.detect_zstandard_dict(os.path.basename(input_dir))

            # Creating the compressor
            zstd_compressor = zstandard.ZstdCompressor(
                dict_data=ZsDic.get_dict(dict_type)
            )

            # Compressing the file data
            file_data = zstd_compressor.compress(file_data)

        # Returning the file
        return file_data

    @staticmethod
    def extract_sarc_to_dir(
            _input: os.PathLike | bytes | typing.BinaryIO,
            out_dir: os.PathLike | str,
            mode: str = "fp",) -> None:
        """
        Extracts SARC files and folders to a directory.

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

                # Creating the SARC controller
                sarc_controller = sarc.SARC(file_data)

                # Extracting the files
                sarc_controller.extract_to_dir(out_dir)

            case "d":

                # Creating the SARC controller
                sarc_controller = sarc.SARC(_input)

                # Extracting the files
                sarc_controller.extract_to_dir(out_dir)

            case "s":

                # Creating SARC controller with file object
                sarc_controller = sarc.read_file_and_make_sarc(_input)

                # Extracting the files
                sarc_controller.extract_to_dir(out_dir)

        return None

    @staticmethod
    def list_sarc_contents(
            _input: os.PathLike | bytes | typing.BinaryIO,
            mode: str) -> list:
        """
        Returns a list of SARC file paths from within a SARC.

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

                # Creating the SARC controller
                sarc_controller = sarc.SARC(file_data)

                # Setting output to the list of files
                output = []

                for key in sarc_controller.list_files().mapping:
                    output.append(key)

            case "d":

                # Creating the SARC controller
                sarc_controller = sarc.SARC(_input)

                # Setting output to the list of files
                output = sarc_controller.list_files()

            case "s":

                # Creating SARC controller with file object
                sarc_controller = sarc.read_file_and_make_sarc(_input)

                # Setting output to the list of files
                output = sarc_controller.list_files()

        return output
