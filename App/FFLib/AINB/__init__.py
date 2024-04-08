# AINB library
from App.FFLib.AINB import converter as conv


# AINB class
class AINB:
    def __init__(self, input_, mode='d'):

        match mode:

            case 'd':

                self.data = input_
                self.json = conv.ainb_to_json(input_, 'd')
                self.yaml = conv.ainb_to_yaml(input_, 'd')

            case 'fp':

                with open(input_, "rb") as f_in:
                    self.data = f_in.read()

                self.json = conv.ainb_to_json(self.data, 'd')
                self.yaml = conv.ainb_to_yaml(self.data, 'd')

    @staticmethod
    def json_to_ainb(json_data):
        return conv.json_to_ainb(json_data, 'd')

    @staticmethod
    def yaml_to_ainb(yaml_data):
        return conv.yaml_to_ainb(yaml_data, 'd')
