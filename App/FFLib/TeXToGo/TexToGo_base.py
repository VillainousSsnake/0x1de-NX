# /App/FFLib/TeXToGo/__init__.py
# Contains TexToGo class

# Importing dependencies
import os
import struct
import zlib
from enum import Enum
import codecs


class FileType(Enum):
    Image = 0


class TXTG:
    def __init__(self, filepath, filename):
        self.FileType = FileType.Image
        self.CanSave = True
        self.Description = ["Texture To Go"]
        self.Extension = ["*.txtg"]
        self.FileName = ""
        self.FilePath = ""
        self.IFileInfo = None
        self.HeaderInfo = None
        self.ImageList = []
        self.Width = 0
        self.Height = 0
        self.ArrayCount = 0
        self.MipCount = 0
        self.Format = None


    def Identify(self, stream):
        signature = stream.read(4)
        return signature == b"P\x00\x11\x00"

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
            self.Hash = [0] * 32
            self.Format = 0
            self.Unknown3 = 0x300
            self.TextureSetting1 = 1116471296
            self.TextureSetting2 = 32563
            self.TextureSetting3 = 33554944
            self.TextureSetting4 = 67330

    class SurfaceInfo:
        def __init__(self):
            self.MipLevel = 0
            self.ArrayLevel = 0
            self.SurfaceCount = 1
            self.Size = 0

    def Load(self, stream):
        self.Tag = self

        self.CanReplace = True

        self.ImageKey = "Texture"
        self.SelectedImageKey = "Texture"

        name = os.path.splitext(os.path.basename(self.FileName))[0]
        self.Text = name

        if name in PluginRuntime.TextureCache:
            del PluginRuntime.TextureCache[name]
        PluginRuntime.TextureCache[name] = self

        reader = FileReader(stream, True)
        reader.SetByteOrder(False)

        self.HeaderInfo = self.Header()
        self.HeaderInfo.HeaderSize = reader.ReadUInt16()
        self.HeaderInfo.Version = reader.ReadUInt16()
        self.HeaderInfo.Magic = reader.ReadBytes(4)
        self.HeaderInfo.Width = reader.ReadUInt16()
        self.HeaderInfo.Height = reader.ReadUInt16()
        self.HeaderInfo.Depth = reader.ReadUInt16()
        self.HeaderInfo.MipCount = reader.ReadByte()
        self.HeaderInfo.Unknown1 = reader.ReadByte()
        self.HeaderInfo.Unknown2 = reader.ReadByte()
        self.HeaderInfo.Padding = reader.ReadUInt16()
        self.HeaderInfo.FormatFlag = reader.ReadByte()
        self.HeaderInfo.FormatSetting = reader.ReadUInt32()
        self.HeaderInfo.CompSelectR = reader.ReadByte()
        self.HeaderInfo.CompSelectG = reader.ReadByte()
        self.HeaderInfo.CompSelectB = reader.ReadByte()
        self.HeaderInfo.CompSelectA = reader.ReadByte()
        self.HeaderInfo.Hash = reader.ReadBytes(32)
        self.HeaderInfo.Format = reader.ReadUInt16()
        self.HeaderInfo.Unknown3 = reader.ReadUInt16()
        self.HeaderInfo.TextureSetting1 = reader.ReadUInt32()
        self.HeaderInfo.TextureSetting2 = reader.ReadUInt32()
        self.HeaderInfo.TextureSetting3 = reader.ReadUInt32()
        self.HeaderInfo.TextureSetting4 = reader.ReadUInt32()

        self.Width = self.HeaderInfo.Width
        self.Height = self.HeaderInfo.Height
        self.ArrayCount = self.HeaderInfo.Depth
        self.MipCount = self.HeaderInfo.MipCount


        surfaces = []
        reader.SeekBegin(self.HeaderInfo.HeaderSize)
        for i in range(self.MipCount * self.ArrayCount):
            surface = self.SurfaceInfo()
            surface.ArrayLevel = reader.ReadUInt16()
            surface.MipLevel = reader.ReadByte()
            reader.ReadByte()
            surfaces.append(surface)

        for i in range(self.MipCount * self.ArrayCount):
            surfaces[i].Size = reader.ReadUInt32()

        data = []
        for i in range(self.MipCount * self.ArrayCount):
            imageData = reader.ReadBytes(surfaces[i].Size)
            if len(data) <= surfaces[i].ArrayLevel:
                data.append([])
            data[surfaces[i].ArrayLevel].append(Zstb.SDecompress(imageData))
            # TODO: Fix error
        self.ImageList = data

    def Save(self, stream):
        self.HeaderInfo.Width = self.Width
        self.HeaderInfo.Height = self.Height
        self.HeaderInfo.Depth = self.ArrayCount
        self.HeaderInfo.MipCount = self.MipCount

        writer = FileWriter(stream)
        writer.WriteUInt16(self.HeaderInfo.HeaderSize)
        writer.WriteUInt16(self.HeaderInfo.Version)
        writer.WriteBytes(self.HeaderInfo.Magic)
        writer.WriteUInt16(self.HeaderInfo.Width)
        writer.WriteUInt16(self.HeaderInfo.Height)
        writer.WriteUInt16(self.HeaderInfo.Depth)
        writer.WriteByte(self.HeaderInfo.MipCount)
        writer.WriteByte(self.HeaderInfo.Unknown1)
        writer.WriteByte(self.HeaderInfo.Unknown2)
        writer.WriteUInt16(self.HeaderInfo.Padding)
        writer.WriteByte(self.HeaderInfo.FormatFlag)
        writer.WriteUInt32(self.HeaderInfo.FormatSetting)
        writer.WriteByte(self.HeaderInfo.CompSelectR)
        writer.WriteByte(self.HeaderInfo.CompSelectG)
        writer.WriteByte(self.HeaderInfo.CompSelectB)
        writer.WriteByte(self.HeaderInfo.CompSelectA)
        writer.WriteBytes(self.HeaderInfo.Hash)
        writer.WriteUInt16(self.HeaderInfo.Format)
        writer.WriteUInt16(self.HeaderInfo.Unknown3)
        writer.WriteUInt32(self.HeaderInfo.TextureSetting1)
        writer.WriteUInt32(self.HeaderInfo.TextureSetting2)
        writer.WriteUInt32(self.HeaderInfo.TextureSetting3)
        writer.WriteUInt32(self.HeaderInfo.TextureSetting4)

        writer.SeekBegin(self.HeaderInfo.HeaderSize)

        surfaceSizes = []
        surfaceData = []

        for mip in range(self.MipCount):
            for array in range(self.ArrayCount):
                writer.WriteUInt16(array)
                writer.WriteByte(mip)
                writer.WriteByte(1)

                surface = Zstb.SCompress(self.ImageList[array][mip], 20)
                surfaceSizes.append(len(surface))
                surfaceData.append(surface)

        for surface in surfaceSizes:
            writer.WriteUInt32(surface)
            writer.WriteUInt32(6)

        for data in surfaceData:
            writer.WriteBytes(data)

    def Dispose(self):
        if self.FileName in PluginRuntime.TextureCache:
            del PluginRuntime.TextureCache[self.FileName]

    def GetImageData(self, ArrayLevel=0, MipLevel=0, DepthLevel=0):
        data = self.ImageList[ArrayLevel][MipLevel]
        return TegraX1Swizzle.GetDirectImageData(self, data, MipLevel)

    def SetImageData(self, bitmap, ArrayLevel):
        tex = TextureData()
        tex.Texture = Syroot.NintenTools.NSW.Bntx.Texture()
        tex.Format = self.Format
        tex.Width = self.Width
        tex.Height = self.Height
        tex.MipCount = self.MipCount
        tex.ArrayCount = self.ArrayCount
        tex.Texture.TextureData = [[]]

        tex.SetImageData(bitmap, ArrayLevel)


class FileReader:
    def __init__(self, stream, isLittleEndian):
        self.stream = stream
        self.isLittleEndian = isLittleEndian

    def SetByteOrder(self, isLittleEndian):
        self.isLittleEndian = isLittleEndian

    def ReadUInt16(self):
        return struct.unpack("<H" if self.isLittleEndian else ">H", self.stream.read(2))[0]

    def ReadUInt32(self):

        if self.isLittleEndian:
            return struct.unpack("<I", codecs.encode(self.stream.read(4), "hex"))[0]
        else:
            return struct.unpack(">I", self.stream.read(4))[0]

    def ReadByte(self):
        return struct.unpack("B", self.stream.read(1))[0]

    def ReadBytes(self, count):
        return self.stream.read(count)

    def SeekBegin(self, offset):
        self.stream.seek(offset, os.SEEK_SET)

    def Position(self):
        return self.stream.tell()


class FileWriter:
    def __init__(self, stream):
        self.stream = stream

    def WriteUInt16(self, value):
        self.stream.write(struct.pack("<H", value))

    def WriteUInt32(self, value):
        self.stream.write(struct.pack("<I", value))

    def WriteByte(self, value):
        self.stream.write(struct.pack("B", value))

    def WriteBytes(self, value):
        self.stream.write(value)

    def SeekBegin(self, offset):
        self.stream.seek(offset, os.SEEK_SET)

class TextureData:
    def __init__(self):
        self.Texture = None
        self.Format = None
        self.Width = 0
        self.Height = 0
        self.MipCount = 0
        self.ArrayCount = 0

    def SetImageData(self, bitmap, ArrayLevel):
        self.Texture.TextureData[0][ArrayLevel] = bitmap.tobytes()

    def Replace(self, FileName, MipCount, ArrayCount, Format, SurfaceDim, Depth):
        self.Texture = Syroot.NintenTools.NSW.Bntx.Texture()
        self.Texture.TextureData = [[]]
        self.Format = Format
        self.Width = 0
        self.Height = 0
        self.MipCount = MipCount
        self.ArrayCount = ArrayCount

    def LoadOpenGLTexture(self):
        pass

class ImageEditorBase:
    def __init__(self):
        self.Text = ""
        self.Width = 0
        self.Height = 0
        self.MipCount = 0
        self.ArrayCount = 0
        self.Format = None

    def LoadProperties(self, prop):
        self.Width = prop.Width
        self.Height = prop.Height
        self.MipCount = prop.MipCount
        self.ArrayCount = prop.ArrayCount
        self.Format = prop.Format

    def LoadImage(self, txtg):
        pass

    def GetArrayDisplayLevel(self):
        return 0

class LibraryGUI:
    @staticmethod
    def GetActiveContent(contentType):
        return None

    @staticmethod
    def LoadEditor(editor):
        pass


class TEX_FORMAT(Enum):
    BC1_UNORM = 0
    BC2_UNORM = 1
    BC3_UNORM = 2
    BC4_UNORM = 3
    BC5_UNORM = 4
    R8_UNORM = 5
    R8G8_UNORM = 6
    R10G10B10A2_UNORM = 7
    B5G6R5_UNORM = 8
    B5G5R5A1_UNORM = 9
    B4G4R4A4_UNORM = 10
    R8G8B8A8_UNORM = 11
    R8G8B8A8_UNORM_SRGB = 12
    ASTC_4x4_UNORM = 13
    ASTC_8x8_UNORM = 14
    ASTC_8x8_SRGB = 15
    ASTC_4x4_SRGB = 16
    BC1_UNORM_SRGB = 17
    BC3_UNORM_SRGB = 18
    BC7_UNORM = 19


class STChannelType(Enum):
    Red = 0
    Green = 1
    Blue = 2
    Alpha = 3
    Zero = 4
    One = 5


class Syroot:
    class NintenTools:
        class NSW:
            class Bntx:
                class Texture:
                    def __init__(self):
                        self.TextureData = None


class TegraX1Swizzle:
    @staticmethod
    def GetDirectImageData(txtg, data, MipLevel):
        return data


class ToolStripMenuItem:
    def __init__(self, text, image, click):
        self.Text = text
        self.Image = image
        self.Click = click


class ToolStripItem:
    pass


class ToolStripSeparator:
    pass


class TreeView:
    pass


class ToolStrip:
    pass


class DockStyle:
    Fill = 0


class PIL:
    class Image:
        class Image:
            def tobytes(self):
                return b""

class PluginRuntime:
    TextureCache = {}

class Magic:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __bytes__(self):
        return self.value

    def __repr__(self):
        return f"Magic({self.value})"

    def __str__(self):
        return self.value