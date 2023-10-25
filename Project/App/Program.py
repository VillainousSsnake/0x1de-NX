# Program Class (V0.0.1)

from Project.App.ProgramFunc.mainMenu import *
from Project.App.ProgramFunc.selectEditor import *
from Project.App.ProgramFunc.settings import *
from Project.App.ProgramFunc.fileEditor import *
from Project.App.ProgramFunc.meshCodecEditor import *
from Project.App.ProgramFunc.gamePathSelect import *


class Program:

    def __init__(self):

        self.returnStatement = None

    def main_menu(self):

        return main_menu(self)

    def select_editor(self):

        return select_editor(self)

    def settings(self):

        return settings(self)

    def game_path_select(self):

        return game_path_select(self)

    def mesh_codec_editor(self):

        return mesh_codec_editor(self)

    def file_editor(self):

        return file_editor(self)
