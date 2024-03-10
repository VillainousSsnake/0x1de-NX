# App/AppLib/index.py
# Contains GUI index

# Importing GUI
from App.GUI.project_editor import project_editor as project_editor_redirect
from App.GUI.main_menu import main_menu as main_menu_redirect


# Index class (Holds menu functions)
class Index:

    @staticmethod
    def main_menu(app):

        main_menu_redirect(app)

    @staticmethod
    def project_editor(app):

        project_editor_redirect(app)
