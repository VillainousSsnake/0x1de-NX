# App/FFLib/custom_sarc.py
# Contains Sarc class

# Importing modules
import zstandard
import tempfile
import os
import sarc


class Sarc:
    def __init__(self, filepath, romfs_path, is_zstd_compressed):

        # Creating self variables
        self.filepath = filepath
        self.romfs_path = romfs_path
        self.is_zstd_compressed = is_zstd_compressed
        with open(self.filepath, "rb") as f_in:
            self.file_controller = sarc.SARC(f_in.read())
        self.file_writer = sarc.make_writer_from_sarc(self.file_controller)

    def add_file(self, path, data):
        self.file_writer.add_file(path, data)

    def add_folder(self, folder_path):
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                full_file_path = os.path.join(root, file_name)
                with open(full_file_path, 'rb') as file:
                    self.file_writer.add_file(file_name, file.read())
        # TODO: Experimental (Test later and remove this)

    def save_sarc(self):
        # Overwriting the sarc
        self.file_writer.write(self.filepath)

        # re-initializing vars
        with open(self.filepath, "rb") as f_in:
            self.file_controller = sarc.SARC(f_in.read())
        self.file_writer = sarc.make_writer_from_sarc(self.file_controller)

    def export_sarc(self):
        pass  # TODO: Stub

    @staticmethod
    def get_zsdic_data(dict_type, romfs_location):

        # Decompressing the ZsDic.pack.zs into ZsDic.pack
        with open(os.path.join(romfs_location, "Pack", "ZsDic.pack.zs"), "rb") as f_in:
            zsdic_archive_data = zstandard.decompress(f_in.read())
        zsdic_archive_controller = sarc.SARC(data=zsdic_archive_data)

        # If statement for the types of zsdics
        if dict_type == ".pack":
            dict_data = zsdic_archive_controller.get_file_data("pack.zsdic")
        elif dict_type == ".byml" or dict_type == ".bcett":
            dict_data = zsdic_archive_controller.get_file_data("bcett.byml.zsdic")
        else:
            dict_data = zsdic_archive_controller.get_file_data("zs.zsdic")

        # Returning dict_data
        return dict_data

    @staticmethod
    def extract_sarc_contents(input_path: str,
                              output_path: str,
                              romfs_location: str,
                              is_zstd_compressed=False,
                              verbose_output=False):

        # Detecting if the file is zstandard compressed
        if is_zstd_compressed:

            # Getting the location of the ZsDic.pack.zs file
            zsdic_comp_arc_location = os.path.join(romfs_location, "Pack", "ZsDic.pack.zs")

            # Reading the file
            with open(zsdic_comp_arc_location, "rb") as f_in:
                zsdic_comp_arc_data = f_in.read()

            # Decompressing the zstd part
            ctrlr = zstandard.ZstdDecompressor()
            zsdic_arc_data = ctrlr.decompress(zsdic_comp_arc_data)

            # Creating temp_dir
            temp_dir = tempfile.TemporaryDirectory()

            # Decompressing all the files into temp_dir
            s_controller = sarc.SARC(data=zsdic_arc_data)
            s_controller.extract_to_dir(temp_dir.name, print_names=verbose_output)

            # Getting the correct dictionary file data
            with open(os.path.join(temp_dir.name, "pack.zsdic"), "rb") as f_stream:
                dict_data = f_stream.read()

            # Deleting temporary directory
            temp_dir.cleanup()

            # Reading the file and decompressing
            with open(input_path, 'rb') as f_in:
                zstd_controller = zstandard.ZstdDecompressor(zstandard.ZstdCompressionDict(dict_data))
                sarc_data = zstd_controller.decompress(f_in.read())

            # Extracting
            controller = sarc.SARC(sarc_data)
            controller.extract_to_dir(output_path, verbose_output)

        else:

            # Reading the file and making sarc
            with open(input_path, 'rb') as f_in:
                controller = sarc.read_file_and_make_sarc(f_in)

            # Extracting
            controller.extract_to_dir(output_path, verbose_output)

    @staticmethod
    def list_root_contents_from_data(sarc_data):

        # Making sarc_controller with sarc_data
        sarc_controller = sarc.SARC(sarc_data)

        # using sarc controller to get sarc_contents
        sarc_contents = list(sarc_controller.list_files())

        # Creating root items
        root_items = []

        # Creating for loop to get the first object in the path for each item in sarc_contents
        for item in sarc_contents:
            if "/" in item:

                # Appending the first folder in the path
                if item.split("/")[0] not in root_items:
                    root_items.append(item.split("/")[0])

            else:

                # Appending the item
                root_items.append(item)

        # Returning root_items
        return sorted(root_items)

    @staticmethod
    def get_contents_of_folder_from_data(sarc_data, folder_path):

        # If the folder path is the root
        if folder_path == "":
            return Sarc.list_root_contents_from_data(sarc_data)

        sarc_controller = sarc.SARC(data=sarc_data)

        # using sarc controller to get sarc_contents
        sarc_contents = list(sarc_controller.list_files())

        # Creating folder_items
        folder_items = list()

        # Getting the paths from the folder
        for item in sarc_contents:
            if folder_path.replace("\\", "/") in item:
                folder_items.append(item)

        # Getting the folders/files from the root of the given folder
        folder_contents = list()
        for path in folder_items:
            if folder_path in path:
                item = path.replace(folder_path, "")
                if "/" in item:
                    item = item.split("/")[0]
                if item not in folder_contents:
                    folder_contents.append(item)

        # Returning folder_contents
        return sorted(folder_contents)

    @staticmethod
    def get_file_size_from_sarc_data(sarc_data: bytes, file_path: str):

        # Creating sarc_controller from sarc_data
        sarc_controller = sarc.SARC(sarc_data)

        # Getting the file data from the file_path
        return sarc_controller.get_file_size(file_path)

    @staticmethod
    def get_contents_of_folder_with_paths_from_data(sarc_data, folder_path):

        # If the folder path is the root
        if folder_path == "":
            sarc_controller = sarc.SARC(sarc_data)
            sarc_contents = list(sarc_controller.list_files())
            return sarc_contents

        # Creating sarc_controller
        sarc_controller = sarc.SARC(data=sarc_data)

        # Using sarc controller to get sarc_contents
        sarc_contents = list(sarc_controller.list_files())

        # Creating folder_items
        folder_items = list()

        # Getting the paths from the folder
        for item in sarc_contents:
            if folder_path.replace("\\", "/") in item:
                folder_items.append(item)

        # Getting the folders/files from the root of the given folder
        folder_contents = list()
        for path in folder_items:
            if folder_path in path:
                if path not in folder_contents:
                    folder_contents.append(path)

        # Returning folder_contents
        return sorted(folder_contents)

    @staticmethod
    def get_file_data_from_sarc_path(sarc_data, path):
        file_controller = sarc.SARC(sarc_data)
        return file_controller.get_file_data(path)

    @staticmethod
    def export_path_from_sarc_data(sarc_data, path):
        pass  # TODO: Stub
