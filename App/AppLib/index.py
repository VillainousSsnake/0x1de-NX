# App/AppLib/index.py
# Contains GUI index

# Importing GUI
from App.GUI.main_menu import main_menu as main_menu_redirect


# Index class (Holds menu functions)
class Index:

    @staticmethod
    def main_menu(app):

        main_menu_redirect(app)


class TexIndex:
    @staticmethod
    def logo_ico():
        pass  # TODO: Stub
