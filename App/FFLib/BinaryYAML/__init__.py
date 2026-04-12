from App.FFLib.BinaryYAML.byml_base import Byml
import json
import yaml
import os


class BYML:
    def __init__(self, file_path: os.PathLike | str) -> None:
        """
        :param file_path: The input file path to the Binary YAML file
        """

        # Detecting if the path is real
        if not os.path.exists(file_path):
            raise FileExistsError("File path given doesn't point to a real file! File path: " + str(file_path))

        # Getting the file data
        with open(file_path, "rb") as f_in:
            raw_data = f_in.read()

        self.byml_controller = Byml(raw_data, filename="file.byml")

    def to_json(self) -> str:
        """
        Converts BYML file data to JSON.
        :return: JSON string
        """
        return self.byml_controller.ToJson()

    def to_yaml(self) -> str:
        """
        Converts BYML file data to YAML.
        :return: YAML string
        """
        return self.byml_controller.ToYaml()

    def to_byml(self, string: str, mode: str = 'yaml') -> bytes:      # TODO: Finish
        """
        Converts JSON or YAML string to BYML Data.
        :param string: JSON or YAML string
        :param mode: Mode for data input type. Can be 'JSON' or 'YAML'
        :return: Converted BYML bytes
        """

        # Getting endian
        endian = None
        match self.byml_controller.bom:
            case ">":
                endian = "big"
            case "<":
                endian = "little"

        # Convert json to yaml if mode is set to json
        if mode.lower() == "json":
            string = yaml.dump(json.loads(string))

        # Return output bytes
        return byml_base.yaml_string_to_byml_bytes(string)
