import io
import struct
from enum import Enum
from typing import List, Any, Type
from PIL import Image


# Required External Libraries (Simulated for Toolbox.Library/VGAudio functionality)
# In a real environment, you would use: pip install zstandard Pillow numpy

# --- Mocking Toolbox.Library and System Dependencies ---

class FileType(Enum):
    Image = 1
    Model = 2
    Archive = 3


class TEX_FORMAT(Enum):
    BC1_UNORM = 0x1
    BC1_UNORM_SRGB = 0x2
    BC2_UNORM = 0x3
    BC3_UNORM = 0x4
    BC3_UNORM_SRGB = 0x5
    BC4_UNORM = 0x6
    BC5_UNORM = 0x7
    BC7_UNORM = 0x8
    R8G8B8A8_UNORM = 0x9
    R8G8B8A8_UNORM_SRGB = 0xA
    R8_UNORM = 0xB
    R8G8_UNORM = 0xC
    R10G10B10A2_UNORM = 0xD
    B5G6R5_UNORM = 0xE
    B5G5R5A1_UNORM = 0xF
    B4G4R4A4_UNORM = 0x10
    ASTC_4x4_UNORM = 0x11
    ASTC_4x4_SRGB = 0x12
    ASTC_8x8_UNORM = 0x13
    ASTC_8x8_SRGB = 0x14
    ASTC_8x5_UNORM = 0x15


class STChannelType(Enum):
    Red = 0
    Green = 1
    Blue = 2
    Alpha = 3
    Zero = 4
    One = 5


class STGenericTexture:
    def __init__(self):
        self.Width = 0
        self.Height = 0
        self.MipCount = 0
        self.ArrayCount = 0
        self.Format = TEX_FORMAT.R8G8B8A8_UNORM
        self.Text = ""
        self.CanEdit = True
        self.IsEdited = False
        self.Tag = None
        self.ImageKey = ""
        self.SelectedImageKey = ""
        self.CanReplace = False
        self.RedChannel = STChannelType.Red
        self.GreenChannel = STChannelType.Green
        self.BlueChannel = STChannelType.Blue
        self.AlphaChannel = STChannelType.Alpha

    @property
    def SupportedFormats(self) -> List[TEX_FORMAT]:
        return []

    def OnClick(self, treeview):
        pass

    def GetImageData(self, ArrayLevel=0, MipLevel=0, DepthLevel=0):
        return b""

    def SetImageData(self, bitmap, ArrayLevel):
        pass

    def Replace(self, FileName):
        pass

    def LoadOpenGLTexture(self):
        pass

    def GetContextMenuItems(self):
        return []


class FileReader:
    def __init__(self, stream, leave_open=False):
        self.stream = stream
        self.leave_open = leave_open
        self.endian = '<'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.leave_open:
            self.stream.close()

    def SetByteOrder(self, big_endian: bool):
        self.endian = '>' if big_endian else '<'

    def CheckSignature(self, offset: int, signature: str, length: int) -> bool:
        pos = self.stream.tell()
        self.stream.seek(offset)
        data = self.stream.read(length).decode('ascii', errors='ignore')
        self.stream.seek(pos)
        return data == signature

    def ReadStruct(self, cls_type):
        # Header Size 0x50
        data = self.stream.read(0x50)
        unpacked = struct.unpack(self.endian + 'HH4sHHHBBBHBI4B32sHHIIII', data)  # Removed H after 4s

        header = cls_type()
        header.HeaderSize = unpacked[0]
        header.Version = unpacked[1]
        header.Magic = unpacked[2].decode('ascii')
        header.Width = unpacked[3]
        header.Height = unpacked[4]
        header.Depth = unpacked[5]
        header.MipCount = unpacked[6]
        header.Unknown1 = unpacked[7]
        header.Unknown2 = unpacked[8]
        header.Padding = unpacked[9]
        header.FormatFlag = unpacked[10]
        header.FormatSetting = unpacked[11]
        header.CompSelectR = unpacked[12]
        header.CompSelectG = unpacked[13]
        header.CompSelectB = unpacked[14]
        header.CompSelectA = unpacked[15]
        header.Hash = unpacked[16]
        header.Format = unpacked[17]
        header.Unknown3 = unpacked[18]
        header.TextureSetting1 = unpacked[19]
        header.TextureSetting2 = unpacked[20]
        header.TextureSetting3 = unpacked[21]
        header.TextureSetting4 = unpacked[22]
        return header

    def ReadUInt16(self):
        return struct.unpack(self.endian + 'H', self.stream.read(2))[0]

    def ReadUInt32(self):
        return struct.unpack(self.endian + 'I', self.stream.read(4))[0]

    def ReadByte(self):
        return struct.unpack('B', self.stream.read(1))[0]

    def ReadBytes(self, count):
        return self.stream.read(count)

    def SeekBegin(self, offset):
        self.stream.seek(offset)

    @property
    def Position(self):
        return self.stream.tell()


class FileWriter:
    def __init__(self, stream):
        self.stream = stream
        self.endian = '<'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def WriteStruct(self, header):
        data = struct.pack(self.endian + 'HH4sHHHBBBHBI4B32sHHIIII',
                           header.HeaderSize, header.Version, header.Magic.encode('ascii'),
                           header.Width, header.Height, header.Depth, header.MipCount,
                           header.Unknown1, header.Unknown2, header.Padding,
                           header.FormatFlag, header.FormatSetting,
                           header.CompSelectR, header.CompSelectG, header.CompSelectB, header.CompSelectA,
                           header.Hash, header.Format, header.Unknown3,
                           header.TextureSetting1, header.TextureSetting2, header.TextureSetting3,
                           header.TextureSetting4)
        self.stream.write(data)

    def Write(self, value):
        if isinstance(value, int):
            if value <= 0xFF:
                self.stream.write(struct.pack('B', value))
            elif value <= 0xFFFF:
                self.stream.write(struct.pack(self.endian + 'H', value))
            else:
                self.stream.write(struct.pack(self.endian + 'I', value))
        elif isinstance(value, bytes):
            self.stream.write(value)

    def SeekBegin(self, offset):
        self.stream.seek(offset)


class Zstb:
    @staticmethod
    def SDecompress(data: bytes) -> bytes:
        # In a real implementation, use import zstandard as zstd
        # return zstd.ZstdDecompressor().decompress(data)
        return data  # Placeholder

    @staticmethod
    def SCompress(data: bytes, level: int) -> bytes:
        # return zstd.ZstdCompressor(level=level).compress(data)
        return data  # Placeholder


class TegraX1Swizzle:
    @staticmethod
    def GetDirectImageData(texture, data, mip_level):
        # Mock logic for swizzling
        return data


class LibraryGUI:
    @staticmethod
    def GetActiveContent(cls_type):
        return None

    @staticmethod
    def LoadEditor(editor):
        pass


class ImageEditorBase:
    def __init__(self):
        self.Dock = None
        self.Text = ""

    def LoadProperties(self, prop):
        pass

    def LoadImage(self, texture):
        pass

    def GetArrayDisplayLevel(self):
        return 0


class PluginRuntime:
    TextureCache = {}


class STFileSaver:
    @staticmethod
    def SaveFileFormat(instance, path):
        with open(path, 'wb') as f:
            instance.Save(f)


class ToolStripMenuItem:
    def __init__(self, text, icon, action):
        self.Text = text
        self.Action = action


class TextureData:
    def __init__(self):
        self.Texture = Any
        self.Format = None
        self.Width = 0
        self.Height = 0
        self.MipCount = 0
        self.ArrayCount = 0

    def SetImageData(self, bitmap, array_level):
        pass

    def Replace(self, file_name, mip_count, arg2, format, dim, arg3):
        pass


# --- Primary Translated Class ---

class TXTG(STGenericTexture):
    def __init__(self):
        super().__init__()
        self.FileType = FileType.Image
        self.CanSave = True
        self.Description = ["Texture To Go"]
        self.Extension = ["*.txtg"]
        self.FileName = ""
        self.FilePath = ""
        self.IFileInfo = None
        self.HeaderInfo = self.Header()
        self.ImageList: List[List[bytes]] = []
        self.CanEdit = True

    def Identify(self, stream: io.BytesIO) -> bool:
        with FileReader(stream, True) as reader:
            return reader.CheckSignature(4, "6PK0", 4)

    @property
    def Types(self) -> List[Type]:
        types = []
        return types

    @property
    def SupportedFormats(self) -> List[TEX_FORMAT]:
        return [
            TEX_FORMAT.BC1_UNORM,
            TEX_FORMAT.BC2_UNORM,
            TEX_FORMAT.BC3_UNORM,
            TEX_FORMAT.BC4_UNORM,
            TEX_FORMAT.BC5_UNORM,
            TEX_FORMAT.R8_UNORM,
            TEX_FORMAT.R8G8_UNORM,
            TEX_FORMAT.R8G8_UNORM,
            TEX_FORMAT.R10G10B10A2_UNORM,
            TEX_FORMAT.B5G6R5_UNORM,
            TEX_FORMAT.B5G5R5A1_UNORM,
            TEX_FORMAT.B4G4R4A4_UNORM,
            TEX_FORMAT.R8G8B8A8_UNORM,
            TEX_FORMAT.R8G8B8A8_UNORM_SRGB,
        ]

    def OnClick(self, treeview):
        self.UpdateEditor()

    def UpdateEditor(self):
        editor = LibraryGUI.GetActiveContent(ImageEditorBase)
        if editor is None:
            editor = ImageEditorBase()
            editor.Dock = "Fill"  # Equivalent to DockStyle.Fill
            LibraryGUI.LoadEditor(editor)

        prop = self.DisplayProperties()
        prop.Width = self.Width
        prop.Height = self.Height
        prop.MipCount = self.MipCount
        prop.ArrayCount = self.ArrayCount
        prop.Format = self.Format
        prop.Hash = "".join(["{:02X}".format(b) for b in self.HeaderInfo.Hash])

        editor.Text = self.Text
        editor.LoadProperties(prop)
        editor.LoadImage(self)

    class Header:
        def __init__(self):
            self.HeaderSize = 0x50
            self.Version = 0x11
            self.Magic = "6PK0"
            self.Width = 0
            self.Height = 0
            self.Depth = 1
            self.MipCount = 0
            self.Unknown1 = 2
            self.Unknown2 = 1
            self.Padding = 0
            self.FormatFlag = 0
            self.FormatSetting = 0
            self.CompSelectR = 0
            self.CompSelectG = 1
            self.CompSelectB = 2
            self.CompSelectA = 3
            self.Hash = bytearray(32)
            self.Format = 0
            self.Unknown3 = 0x300
            self.TextureSetting1 = 1116471296
            self.TextureSetting2 = 32563
            self.TextureSetting3 = 33554944
            self.TextureSetting4 = 67330

    def GetContextMenuItems(self):
        items = []
        items.append(ToolStripMenuItem("Save File", None, lambda o, e: STFileSaver.SaveFileFormat(self, self.FilePath)))
        items.extend(super().GetContextMenuItems())
        return items

    def Load(self, stream: io.BytesIO):
        self.Tag = self
        self.CanReplace = True
        self.ImageKey = "Texture"
        self.SelectedImageKey = "Texture"

        import os
        name = os.path.splitext(os.path.basename(self.FileName))[0]
        self.Text = name

        if name in PluginRuntime.TextureCache:
            del PluginRuntime.TextureCache[name]

        PluginRuntime.TextureCache[name] = self

        with FileReader(stream, True) as reader:
            reader.SetByteOrder(False)
            self.HeaderInfo = reader.ReadStruct(self.Header)

            self.Width = self.HeaderInfo.Width
            self.Height = self.HeaderInfo.Height
            self.ArrayCount = self.HeaderInfo.Depth
            self.MipCount = self.HeaderInfo.MipCount

            self.RedChannel = TXTG.ChannelList[self.HeaderInfo.CompSelectR]
            self.GreenChannel = TXTG.ChannelList[self.HeaderInfo.CompSelectG]
            self.BlueChannel = TXTG.ChannelList[self.HeaderInfo.CompSelectB]
            self.AlphaChannel = TXTG.ChannelList[self.HeaderInfo.CompSelectA]

            surfaces = [self.SurfaceInfo() for _ in range(self.MipCount * self.ArrayCount)]

            reader.SeekBegin(self.HeaderInfo.HeaderSize)
            for i in range(self.MipCount * self.ArrayCount):
                surfaces[i].ArrayLevel = reader.ReadUInt16()
                surfaces[i].MipLevel = reader.ReadByte()
                reader.ReadByte()  # Always 1

            for i in range(self.MipCount * self.ArrayCount):
                surfaces[i].Size = reader.ReadUInt32()
                reader.ReadUInt32()  # Always 6

            if self.HeaderInfo.Format in TXTG.FormatList:
                self.Format = TXTG.FormatList[self.HeaderInfo.Format]
            else:
                raise Exception("Unsupported format! {}".format(hex(self.HeaderInfo.Format)))

            if self.HeaderInfo.TextureSetting2 == 32628:
                self.Format = TEX_FORMAT.ASTC_8x5_UNORM
            if self.HeaderInfo.TextureSetting2 == 32631:
                self.Format = TEX_FORMAT.ASTC_8x8_UNORM

            data: List[List[bytes]] = []

            for i in range(self.MipCount * self.ArrayCount):
                image_data = reader.ReadBytes(int(surfaces[i].Size))

                while len(data) <= surfaces[i].ArrayLevel:
                    data.append([])

                data[surfaces[i].ArrayLevel].append(Zstb.SDecompress(image_data))

            self.ImageList = data

    def Save(self, stream: io.BytesIO):
        # Apply generic properties
        for k, v in TXTG.FormatList.items():
            if v == self.Format:
                self.HeaderInfo.Format = k
                break

        self.HeaderInfo.Width = int(self.Width)
        self.HeaderInfo.Height = int(self.Height)
        self.HeaderInfo.Depth = int(self.ArrayCount)
        self.HeaderInfo.MipCount = int(self.MipCount)

        with FileWriter(stream) as writer:
            writer.WriteStruct(self.HeaderInfo)
            writer.SeekBegin(self.HeaderInfo.HeaderSize)

            surfaceSizes = []
            surfaceData = []

            for mip in range(self.MipCount):
                for array in range(self.ArrayCount):
                    writer.Write(array)  # ushort
                    writer.Write(mip)  # byte
                    writer.Write(1)  # byte

                    surface = Zstb.SCompress(self.ImageList[array][mip], 20)
                    surfaceSizes.append(len(surface))
                    surfaceData.append(surface)

            for size in surfaceSizes:
                writer.Write(size)  # uint
                writer.Write(6)  # uint

            for data in surfaceData:
                writer.Write(data)

    def Dispose(self):
        if self.FileName in PluginRuntime.TextureCache:
            del PluginRuntime.TextureCache[self.FileName]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Dispose()

    def GetImageData(self, ArrayLevel=0, MipLevel=0, DepthLevel=0):
        data = self.ImageList[ArrayLevel][MipLevel]
        return TegraX1Swizzle.GetDirectImageData(self, data, MipLevel)

    def SetImageData(self, bitmap: Image.Image, ArrayLevel: int):
        tex = TextureData()
        tex.Texture = type('obj', (object,), {'TextureData': []})()  # Mock object
        tex.Format = self.Format
        tex.Width = self.Width
        tex.Height = self.Height
        tex.MipCount = self.MipCount
        tex.ArrayCount = self.ArrayCount
        tex.Texture.TextureData = [[]]

        tex.SetImageData(bitmap, ArrayLevel)
        self.SetImage(tex, ArrayLevel)

    def Replace(self, FileName: str):
        tex = TextureData()
        # Mocking Syroot.NintenTools.NSW.Bntx.GFX.SurfaceDim.Dim2D as 1
        tex.Replace(FileName, self.MipCount, 0, self.Format, 1, 1)

        editor = LibraryGUI.GetActiveContent(ImageEditorBase)
        targetArray = 0
        if editor is not None:
            targetArray = editor.GetArrayDisplayLevel()

        self.SetImage(tex, targetArray)

    def SetImage(self, tex: TextureData, targetArray: int):
        if tex.Texture is None:
            return

        for i in range(len(self.ImageList[0])):
            print("SIZE 1 mip{} {}".format(i, len(self.ImageList[0][i])))

        if len(self.ImageList) > 1 and self.Format != tex.Format:
            raise Exception(
                "Imported texture must use the original format for surface injecting! Expected {} but got {}! If you need ASTC, use an astc encoder with .astc file format.".format(
                    self.Format, tex.Format))

        if len(tex.Texture.TextureData) == 1:
            self.ImageList[targetArray] = tex.Texture.TextureData[0]
        else:
            self.ImageList.clear()
            for surface in tex.Texture.TextureData:
                self.ImageList.append(surface)

        for i in range(len(self.ImageList[0])):
            print("SIZE 2 mip{} {}".format(i, len(self.ImageList[0][i])))

        self.Width = tex.Texture.Width if hasattr(tex.Texture, 'Width') else self.Width
        self.Height = tex.Texture.Height if hasattr(tex.Texture, 'Height') else self.Height
        self.MipCount = tex.Texture.MipCount if hasattr(tex.Texture, 'MipCount') else self.MipCount
        self.ArrayCount = len(self.ImageList)
        self.Format = tex.Format

        self.IsEdited = True
        self.UpdateEditor()
        self.LoadOpenGLTexture()

    class SurfaceInfo:
        def __init__(self):
            self.MipLevel = 0
            self.ArrayLevel = 0
            self.SurfaceCount = 1
            self.Size = 0

    ChannelList = {
        0: STChannelType.Red,
        1: STChannelType.Green,
        2: STChannelType.Blue,
        3: STChannelType.Alpha,
        4: STChannelType.Zero,
        5: STChannelType.One,
    }

    FormatList = {
        0x101: TEX_FORMAT.ASTC_4x4_UNORM,
        0x102: TEX_FORMAT.ASTC_8x8_UNORM,
        0x105: TEX_FORMAT.ASTC_8x8_SRGB,
        0x109: TEX_FORMAT.ASTC_4x4_SRGB,
        0x202: TEX_FORMAT.BC1_UNORM,
        0x203: TEX_FORMAT.BC1_UNORM_SRGB,
        0x302: TEX_FORMAT.BC1_UNORM,
        0x505: TEX_FORMAT.BC3_UNORM_SRGB,
        0x602: TEX_FORMAT.BC4_UNORM,
        0x606: TEX_FORMAT.BC4_UNORM,
        0x607: TEX_FORMAT.BC4_UNORM,
        0x702: TEX_FORMAT.BC5_UNORM,
        0x703: TEX_FORMAT.BC5_UNORM,
        0x707: TEX_FORMAT.BC5_UNORM,
        0x901: TEX_FORMAT.BC7_UNORM,
    }

    class DisplayProperties:
        def __init__(self):
            self.Height = 0
            self.Width = 0
            self.Format = TEX_FORMAT.R8G8B8A8_UNORM
            self.MipCount = 0
            self.ArrayCount = 0
            self.Hash = ""

