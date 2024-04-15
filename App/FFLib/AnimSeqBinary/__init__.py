# /App/FFLib/AinimSeqBinary/__init__.py
# Contains ASB class

# Importing modules, libraries, and packages
from App.FFLib.AnimSeqBinary import asb_dt
import os


# ASB Class
class ASB:
    def __init__(self, file_path):

        # Creating file path variable
        self.file_path = file_path
