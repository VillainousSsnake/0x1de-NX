# Program Class (V0.0.1)

from Project.App.ProgramFunc.mainMenu import *
from Project.App.ProgramFunc.selectEditor import *
from Project.App.ProgramFunc.settings import *
from Project.App.ProgramFunc.fileEditor import *
from Project.App.ProgramFunc.meshCodecEditor import *
from Project.App.ProgramFunc.gamePathSelect import *
from Project.App.ProgramFunc.displayErrorCode import *
from Project.App.ProgramFunc.pluginsMenu import *


class Program:

    def __init__(self):

        self.returnStatement = None

    def display_error_code(self, error_code, error_details):

        return display_error_code(self, error_code, error_details)

    def file_editor(self):

        return file_editor(self)

    def game_path_select(self):

        return game_path_select(self)

    def main_menu(self):

        return main_menu(self)

    def mesh_codec_editor(self):

        return mesh_codec_editor(self)

    def plugins_menu(self):

        return plugins_menu(self)

    def select_editor(self):

        return select_editor(self)

    def settings(self):

        return settings(self)
