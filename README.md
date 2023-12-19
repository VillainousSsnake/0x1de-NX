# 0x1de-NX

## NOTICE:
Please note that there are currently no releases for this app. 0x1de-NX is still in development. However, the source code is avalible to the public through this repository. If you want to install Python 3.11 and run the project yourself, dont expect any of the features to work or even be implemented though. If you do plan to run the application, see "Installation and Setup (From Source Code)" to do so.

### LATEST VERSION: 
0.0.1

### DESCRIPTION:
0x1de NX is a modding tool for Zelda: Tears of the Kingdom modders that aims to make modding and playing/managing mods as simple and easy as possible.

### Planned Features:
- **Mesh editor** for **MeshCodec Packages** (.mc files)
- **File Format Editor** for **all *Legend of Zelda: Tears of the Kingdom* File Formats**
- **Mod Merger** so you can **Merge *Any* Mods**

### Installation and Setup (From Source Code):
NOTE: The source code has only been run with a Windows 11 PC, but may work for Mac and Linux

Requirements:
- Python 3.11 or later (https://python.org)
- Latest version of pip installer (You can install pip with the Python Installer)
- A dump of Zelda: Tears of the Kingdom
- totkzstdtool (https://github.com/TotkMods/Totk.ZStdTool)
- SARCExtract (https://github.com/aboood40091/SARCExtract)

#### Part 1. Installing pip Dependencies:
Run the '0x1de-NX-INSTALLER.py' file and it will install all the pip dependencies for you.

#### Part 2. Downloading, extracting and setting up the zip:
Download the source code as a zip file, then extract it to a folder anywhere on your computer (just put it in a folder anywhere) then delete the zip file after you extracted it (if you want)

#### Part 3. Setting up the `.zsdic` files:
Go to your Zelda: Tears of the Kingdom romfs dump and copy the file in `romfs/Pack/` called `ZsDic.pack.zs` to a safe place on your computer. Then extract it using totkzstdtool to get the `ZsDic.pack`. Then with SARCExtract extract the `ZsDic.pack` file to get your `.zsdic` files. Now that you have you `.zsdic` files, copy all of them and go to the folder you extracted 0x1de-NX's source code in and open it. Then go to `Project/__Cache__/` and create a folder called `_dict_`. Then paste all of your `.zsdic` files into that folder.

#### Part 4. Running the app:
Double click `main.py`. It should be in the folder you extracted 0x1de-NX's source code in. Enjoy using 0x1de-NX! Also you have to repeat this every time you want to update the app.


### Please join the discord!
link: https://discord.gg/GA5qfJ53bK









