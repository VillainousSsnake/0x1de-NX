"""
INSTALLER VERSION: v1.0
INSTALLS 0x1de-NX VERSION: v0.0.1
"""

import subprocess
import sys

# Terms of service:
import tkinter as tk
from tkinter import scrolledtext
returnStatement = None


def accept():
    global returnStatement
    returnStatement = "accept"
    root.destroy()


def decline():
    global returnStatement
    returnStatement = "decline"
    root.destroy()


root = tk.Tk()
root.title("Terms of Service")
root.protocol("WM_DELETE_WINDOW", decline)
scroll_text = scrolledtext.ScrolledText(root, width=50, height=20)
scroll_text.pack()
terms_of_service = """
-- 0x1de NX Installer --

Stub
.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n
.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n
.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n
.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n
Stub
"""
scroll_text.insert(tk.INSERT, terms_of_service)
scroll_text.config(state="disabled")
accept_button = tk.Button(root, text="Accept", command=accept)
accept_button.pack()
decline_button = tk.Button(root, text="Decline", command=decline)
decline_button.pack()
root.mainloop()

while returnStatement is None:
    pass
if returnStatement == "decline":
    exit(0)


# Output
print(" -- 0x1de NX Installer --\n")
print("""If there are ANY errors, please make sure you have Python 3.11.7 installed.
 If you have Python 3.11.7 and you are still getting errors, please submit a bug report in the official 0x1de-NX discord
  Discord Server: https://discord.gg/GA5qfJ53bK""")

# Installing pip packages
print("Installing dependencies...")


# Defining the installation function
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


for pk in ["SarcLib", "sarc", "zstandard", "rstb"]:
    install(pk)


# Output
print("Finished Installing Dependencies!\nRunning main.py...")

# Running main.py
subprocess.run([sys.executable, "main.py"])

# Output
print("Ran main.py!\nExiting the app...")
