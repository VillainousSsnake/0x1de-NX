# /App/FFLib/TeXToGo/__init__.py
# Contains TexToGo class

# Importing dependencies
import sys
import os
import struct
import zlib
from enum import Enum
from PIL import Image


class FileType(Enum):
    Image = 0


class TXTG:
    def __init__(self):
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
        return signature == b"6PK0"

    def Types(self):
        return []

    def CanEdit(self):
        return True

    def SupportedFormats(self):
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
        pass    # TODO: Stub

    def UpdateEditor(self):
        pass    # TODO: Stub

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

    class DisplayProperties:
        def __init__(self):
            self.Height = 0
            self.Width = 0
            self.Format = None
            self.MipCount = 0
            self.ArrayCount = 0
            self.Hash = ""

    def GetContextMenuItems(self):
        items = []
        items.append(ToolStripMenuItem("Save File", None, lambda o, e: STFileSaver.SaveFileFormat(self, self.FilePath)))
        items.extend(base.GetContextMenuItems())
        return items

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

        self.RedChannel = ChannelList[self.HeaderInfo.CompSelectR]
        self.GreenChannel = ChannelList[self.HeaderInfo.CompSelectG]
        self.BlueChannel = ChannelList[self.HeaderInfo.CompSelectB]
        self.AlphaChannel = ChannelList[self.HeaderInfo.CompSelectA]

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
            reader.ReadUInt32()

        pos = reader.Position

        if self.HeaderInfo.Format in FormatList:
            self.Format = FormatList[self.HeaderInfo.Format]
        else:
            raise Exception(f"Unsupported format! {self.HeaderInfo.Format:X}")

        data = []
        for i in range(self.MipCount * self.ArrayCount):
            imageData = reader.ReadBytes(surfaces[i].Size)
            if len(data) <= surfaces[i].ArrayLevel:
                data.append([])
            data[surfaces[i].ArrayLevel].append(Zstb.SDecompress(imageData))
        self.ImageList = data

    def Save(self, stream):
        self.HeaderInfo.Format = next((k for k, v in FormatList.items() if v == self.Format), None)
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
        self.SetImage(tex, ArrayLevel)

    def Replace(self, FileName):
        tex = TextureData()
        tex.Replace(FileName, self.MipCount, 0, self.Format, Syroot.NintenTools.NSW.Bntx.GFX.SurfaceDim.Dim2D, 1)

        editor = LibraryGUI.GetActiveContent(ImageEditorBase)
        targetArray = 0
        if editor is not None:
            targetArray = editor.GetArrayDisplayLevel()

        self.SetImage(tex, targetArray)

    def SetImage(self, tex, targetArray):
        if tex.Texture is None:
            return

        for i in range(len(self.ImageList[0])):
            print(f"SIZE 1 mip{i} {len(self.ImageList[0][i])}")

        if len(self.ImageList) > 1 and self.Format != tex.Format:
            raise Exception(f"Imported texture must use the original format for surface injecting! Expected {self.Format} but got {tex.Format}! If you need ASTC, use an astc encoder with .astc file format.")

        if len(tex.Texture.TextureData) == 1:
            self.ImageList[targetArray] = tex.Texture.TextureData[0]
        else:
            self.ImageList.clear()
            self.ImageList.extend(tex.Texture.TextureData)

        for i in range(len(self.ImageList[0])):
            print(f"SIZE 2 mip{i} {len(self.ImageList[0][i])}")

        self.Width = tex.Texture.Width
        self.Height = tex.Texture.Height
        self.MipCount = tex.Texture.MipCount
        self.ArrayCount = len(self.ImageList)
        self.Format = tex.Format

        self.IsEdited = True

        self.UpdateEditor()

        self.LoadOpenGLTexture()

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

class FileReader:
    def __init__(self, stream, isLittleEndian):
        self.stream = stream
        self.isLittleEndian = isLittleEndian

    def SetByteOrder(self, isLittleEndian):
        self.isLittleEndian = isLittleEndian

    def ReadUInt16(self):
        return struct.unpack("<H" if self.isLittleEndian else ">H", self.stream.read(2))[0]

    def ReadUInt32(self):
        return struct.unpack("<I" if self.isLittleEndian else ">I", self.stream.read(4))[0]

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

class Zstb:
    @staticmethod
    def SDecompress(data):
        return zlib.decompress(data)

    @staticmethod
    def SCompress(data, level):
        return zlib.compress(data, level)

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

class STFileSaver:
    @staticmethod
    def SaveFileFormat(txtg, FilePath):
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

class Image:
    @staticmethod
    def open(filename):
        return Image()

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

def TXTG():
    return TXTG()

def FileType():
    return FileType()

def CanSave():
    return True

def Description():
    return ["Texture To Go"]

def Extension():
    return ["*.txtg"]

def FileName():
    return ""

def FilePath():
    return ""

def IFileInfo():
    return None

def Identify(stream):
    signature = stream.read(4)
    return signature == b"6PK0"

def Types():
    return []

def CanEdit():
    return True

def SupportedFormats():
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

def OnClick(treeview):
    UpdateEditor()

def UpdateEditor():
    editor = LibraryGUI.GetActiveContent(ImageEditorBase)
    if editor is None:
        editor = ImageEditorBase()
        editor.Dock = DockStyle.Fill
        LibraryGUI.LoadEditor(editor)

    prop = DisplayProperties()
    prop.Width = Width
    prop.Height = Height
    prop.MipCount = MipCount
    prop.ArrayCount = ArrayCount
    prop.Format = Format
    prop.Hash = "".join([format(x, "X2") for x in HeaderInfo.Hash])

    editor.Text = Text
    editor.LoadProperties(prop)
    editor.LoadImage(self)

def GetContextMenuItems():
    items = []
    items.append(ToolStripMenuItem("Save File", None, lambda o, e: STFileSaver.SaveFileFormat(self, FilePath)))
    items.extend(base.GetContextMenuItems())
    return items

def Load(stream):
    Tag = self

    CanReplace = True

    ImageKey = "Texture"
    SelectedImageKey = "Texture"

    name = os.path.splitext(os.path.basename(FileName))[0]
    Text = name

    if name in PluginRuntime.TextureCache:
        del PluginRuntime.TextureCache[name]
    PluginRuntime.TextureCache[name] = self

    reader = FileReader(stream, True)
    reader.SetByteOrder(False)

    HeaderInfo = Header()
    HeaderInfo.HeaderSize = reader.ReadUInt16()
    HeaderInfo.Version = reader.ReadUInt16()
    HeaderInfo.Magic = reader.ReadBytes(4)
    HeaderInfo.Width = reader.ReadUInt16()
    HeaderInfo.Height = reader.ReadUInt16()
    HeaderInfo.Depth = reader.ReadUInt16()
    HeaderInfo.MipCount = reader.ReadByte()
    HeaderInfo.Unknown1 = reader.ReadByte()
    HeaderInfo.Unknown2 = reader.ReadByte()
    HeaderInfo.Padding = reader.ReadUInt16()
    HeaderInfo.FormatFlag = reader.ReadByte()
    HeaderInfo.FormatSetting = reader.ReadUInt32()
    HeaderInfo.CompSelectR = reader.ReadByte()
    HeaderInfo.CompSelectG = reader.ReadByte()
    HeaderInfo.CompSelectB = reader.ReadByte()
    HeaderInfo.CompSelectA = reader.ReadByte()
    HeaderInfo.Hash = reader.ReadBytes(32)
    HeaderInfo.Format = reader.ReadUInt16()
    HeaderInfo.Unknown3 = reader.ReadUInt16()
    HeaderInfo.TextureSetting1 = reader.ReadUInt32()
    HeaderInfo.TextureSetting2 = reader.ReadUInt32()
    HeaderInfo.TextureSetting3 = reader.ReadUInt32()
    HeaderInfo.TextureSetting4 = reader.ReadUInt32()

    Width = HeaderInfo.Width
    Height = HeaderInfo.Height
    ArrayCount = HeaderInfo.Depth
    MipCount = HeaderInfo.MipCount

    RedChannel = ChannelList[HeaderInfo.CompSelectR]
    GreenChannel = ChannelList[HeaderInfo.CompSelectG]
    BlueChannel = ChannelList[HeaderInfo.CompSelectB]
    AlphaChannel = ChannelList[HeaderInfo.CompSelectA]

    surfaces = []
    reader.SeekBegin(HeaderInfo.HeaderSize)
    for i in range(MipCount * ArrayCount):
        surface = SurfaceInfo()
        surface.ArrayLevel = reader.ReadUInt16()
        surface.MipLevel = reader.ReadByte()
        reader.ReadByte()
        surfaces.append(surface)

    for i in range(MipCount * ArrayCount):
        surfaces[i].Size = reader.ReadUInt32()
        reader.ReadUInt32()

    pos = reader.Position

    if HeaderInfo.Format in FormatList:
        Format = FormatList[HeaderInfo.Format]
    else:
        raise Exception(f"Unsupported format! {HeaderInfo.Format:X}")

    data = []
    for i in range(MipCount * ArrayCount):
        imageData = reader.ReadBytes(surfaces[i].Size)
        if len(data) <= surfaces[i].ArrayLevel:
            data.append([])
        data[surfaces[i].ArrayLevel].append(Zstb.SDecompress(imageData))
    ImageList = data

def Save(stream):
    HeaderInfo.Format = next((k for k, v in FormatList.items() if v == Format), None)
    HeaderInfo.Width = Width
    HeaderInfo.Height = Height
    HeaderInfo.Depth = ArrayCount
    HeaderInfo.MipCount = MipCount

    writer = FileWriter(stream)
    writer.WriteUInt16(HeaderInfo.HeaderSize)
    writer.WriteUInt16(HeaderInfo.Version)
    writer.WriteBytes(HeaderInfo.Magic)
    writer.WriteUInt16(HeaderInfo.Width)
    writer.WriteUInt16(HeaderInfo.Height)
    writer.WriteUInt16(HeaderInfo.Depth)
    writer.WriteByte(HeaderInfo.MipCount)
    writer.WriteByte(HeaderInfo.Unknown1)
    writer.WriteByte(HeaderInfo.Unknown2)
    writer.WriteUInt16(HeaderInfo.Padding)
    writer.WriteByte(HeaderInfo.FormatFlag)
    writer.WriteUInt32(HeaderInfo.FormatSetting)
    writer.WriteByte(HeaderInfo.CompSelectR)
    writer.WriteByte(HeaderInfo.CompSelectG)
    writer.WriteByte(HeaderInfo.CompSelectB)
    writer.WriteByte(HeaderInfo.CompSelectA)
    writer.WriteBytes(HeaderInfo.Hash)
    writer.WriteUInt16(HeaderInfo.Format)
    writer.WriteUInt16(HeaderInfo.Unknown3)
    writer.WriteUInt32(HeaderInfo.TextureSetting1)
    writer.WriteUInt32(HeaderInfo.TextureSetting2)
    writer.WriteUInt32(HeaderInfo.TextureSetting3)
    writer.WriteUInt32(HeaderInfo.TextureSetting4)

    writer.SeekBegin(HeaderInfo.HeaderSize)

    surfaceSizes = []
    surfaceData = []

    for mip in range(MipCount):
        for array in range(ArrayCount):
            writer.WriteUInt16(array)
            writer.WriteByte(mip)
            writer.WriteByte(1)

            surface = Zstb.SCompress(ImageList[array][mip], 20)
            surfaceSizes.append(len(surface))
            surfaceData.append(surface)

    for surface in surfaceSizes:
        writer.WriteUInt32(surface)
        writer.WriteUInt32(6)

    for data in surfaceData:
        writer.WriteBytes(data)

def Dispose():
    if FileName in PluginRuntime.TextureCache:
        del PluginRuntime.TextureCache[FileName]

def GetImageData(ArrayLevel=0, MipLevel=0, DepthLevel=0):
    data = ImageList[ArrayLevel][MipLevel]
    return TegraX1Swizzle.GetDirectImageData(self, data, MipLevel)

def SetImageData(bitmap, ArrayLevel):
    tex = TextureData()
    tex.Texture = Syroot.NintenTools.NSW.Bntx.Texture()
    tex.Format = Format
    tex.Width = Width
    tex.Height = Height
    tex.MipCount = MipCount
    tex.ArrayCount = ArrayCount
    tex.Texture.TextureData = [[]]

    tex.SetImageData(bitmap, ArrayLevel)
    SetImage(tex, ArrayLevel)

def Replace(FileName):
    tex = TextureData()
    tex.Replace(FileName, MipCount, 0, Format, Syroot.NintenTools.NSW.Bntx.GFX.SurfaceDim.Dim2D, 1)

    editor = LibraryGUI.GetActiveContent(ImageEditorBase)
    targetArray = 0
    if editor is not None:
        targetArray = editor.GetArrayDisplayLevel()

    SetImage(tex, targetArray)

def SetImage(tex, targetArray):
    if tex.Texture is None:
        return

    for i in range(len(ImageList[0])):
        print(f"SIZE 1 mip{i} {len(ImageList[0][i])}")

    if len(ImageList) > 1 and Format != tex.Format:
        raise Exception(f"Imported texture must use the original format for surface injecting! Expected {Format} but got {tex.Format}! If you need ASTC, use an astc encoder with .astc file format.")

    if len(tex.Texture.TextureData) == 1:
        ImageList[targetArray] = tex.Texture.TextureData[0]
    else:
        ImageList.clear()
        ImageList.extend(tex.Texture.TextureData)

    for i in range(len(ImageList[0])):
        print(f"SIZE 2 mip{i} {len(ImageList[0][i])}")

    Width = tex.Texture.Width
    Height = tex.Texture.Height
    MipCount = tex.Texture.MipCount
    ArrayCount = len(ImageList)
    Format = tex.Format

    IsEdited = True

    UpdateEditor()

    LoadOpenGLTexture()

def GetActiveContent(contentType):
    return None

def LoadEditor(editor):
    pass

def SaveFileFormat(txtg, FilePath):
    pass

def GetDirectImageData(txtg, data, MipLevel):
    return data

def open(filename):
    return Image()

def tobytes(self):
    return b""

def TXTG():
    return TXTG()

def FileType():
    return FileType()

def CanSave():
    return True

def Description():
    return ["Texture To Go"]

def Extension():
    return ["*.txtg"]

def FileName():
    return ""

def FilePath():
    return ""

def IFileInfo():
    return None

def Identify(stream):
    signature = stream.read(4)
    return signature == b"6PK0"

def Types():
    return []

def CanEdit():
    return True

def SupportedFormats():
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

def OnClick(treeview):
    UpdateEditor()

def UpdateEditor():
    editor = LibraryGUI.GetActiveContent(ImageEditorBase)
    if editor is None:
        editor = ImageEditorBase()
        editor.Dock = DockStyle.Fill
        LibraryGUI.LoadEditor(editor)

    prop = DisplayProperties()
    prop.Width = Width
    prop.Height = Height
    prop.MipCount = MipCount
    prop.ArrayCount = ArrayCount
    prop.Format = Format
    prop.Hash = "".join([format(x, "X2") for x in HeaderInfo.Hash])

    editor.Text = Text
    editor.LoadProperties(prop)
    editor.LoadImage(self)

def GetContextMenuItems():
    items = []
    items.append(ToolStripMenuItem("Save File", None, lambda o, e: STFileSaver.SaveFileFormat(self, FilePath)))
    items.extend(base.GetContextMenuItems())
    return items

def Load(stream):
    Tag = self

    CanReplace = True

    ImageKey = "Texture"
    SelectedImageKey = "Texture"

    name = os.path.splitext(os.path.basename(FileName))[0]
    Text = name

    if name in PluginRuntime.TextureCache:
        del PluginRuntime.TextureCache[name]
    PluginRuntime.TextureCache[name] = self

    reader = FileReader(stream, True)
    reader.SetByteOrder(False)

    HeaderInfo = Header()
    HeaderInfo.HeaderSize = reader.ReadUInt16()
    HeaderInfo.Version = reader.ReadUInt16()
    HeaderInfo.Magic = reader.ReadBytes(4)
    HeaderInfo.Width = reader.ReadUInt16()
    HeaderInfo.Height = reader.ReadUInt16()
    HeaderInfo.Depth = reader.ReadUInt16()
    HeaderInfo.MipCount = reader.ReadByte()
    HeaderInfo.Unknown1 = reader.ReadByte()
    HeaderInfo.Unknown2 = reader.ReadByte()
    HeaderInfo.Padding = reader.ReadUInt16()
    HeaderInfo.FormatFlag = reader.ReadByte()
    HeaderInfo.FormatSetting = reader.ReadUInt32()
    HeaderInfo.CompSelectR = reader.ReadByte()
    HeaderInfo.CompSelectG = reader.ReadByte()
    HeaderInfo.CompSelectB = reader.ReadByte()
    HeaderInfo.CompSelectA = reader.ReadByte()
    HeaderInfo.Hash = reader.ReadBytes(32)
    HeaderInfo.Format = reader.ReadUInt16()
    HeaderInfo.Unknown3 = reader.ReadUInt16()
    HeaderInfo.TextureSetting1 = reader.ReadUInt32()
    HeaderInfo.TextureSetting2 = reader.ReadUInt32()
    HeaderInfo.TextureSetting3 = reader.ReadUInt32()
    HeaderInfo.TextureSetting4 = reader.ReadUInt32()

    Width = HeaderInfo.Width
    Height = HeaderInfo.Height
    ArrayCount = HeaderInfo.Depth
    MipCount = HeaderInfo.MipCount

    RedChannel = ChannelList[HeaderInfo.CompSelectR]
    GreenChannel = ChannelList[HeaderInfo.CompSelectG]
    BlueChannel = ChannelList[HeaderInfo.CompSelectB]
    AlphaChannel = ChannelList[HeaderInfo.CompSelectA]

    surfaces = []
    reader.SeekBegin(HeaderInfo.HeaderSize)
    for i in range(MipCount * ArrayCount):
        surface = SurfaceInfo()
        surface.ArrayLevel = reader.ReadUInt16()
        surface.MipLevel = reader.ReadByte()
        reader.ReadByte()
        surfaces.append(surface)

    for i in range(MipCount * ArrayCount):
        surfaces[i].Size = reader.ReadUInt32()
        reader.ReadUInt32()

    pos = reader.Position

    if HeaderInfo.Format in FormatList:
        Format = FormatList[HeaderInfo.Format]
    else:
        raise Exception(f"Unsupported format! {HeaderInfo.Format:X}")

    data = []
    for i in range(MipCount * ArrayCount):
        imageData = reader.ReadBytes(surfaces[i].Size)
        if len(data) <= surfaces[i].ArrayLevel:
            data.append([])
        data[surfaces[i].ArrayLevel].append(Zstb.SDecompress(imageData))
    ImageList = data

def Save(stream):
    HeaderInfo.Format = next((k for k, v in FormatList.items() if v == Format), None)
    HeaderInfo.Width = Width
    HeaderInfo.Height = Height
    HeaderInfo.Depth = ArrayCount
    HeaderInfo.MipCount = MipCount

    writer = FileWriter(stream)
    writer.WriteUInt16(HeaderInfo.HeaderSize)
    writer.WriteUInt16(HeaderInfo.Version)
    writer.WriteBytes(HeaderInfo.Magic)
    writer.WriteUInt16(HeaderInfo.Width)
    writer.WriteUInt16(HeaderInfo.Height)
    writer.WriteUInt16(HeaderInfo.Depth)
    writer.WriteByte(HeaderInfo.MipCount)
    writer.WriteByte(HeaderInfo.Unknown1)
    writer.WriteByte(HeaderInfo.Unknown2)
    writer.WriteUInt16(HeaderInfo.Padding)
    writer.WriteByte(HeaderInfo.FormatFlag)
    writer.WriteUInt32(HeaderInfo.FormatSetting)
    writer.WriteByte(HeaderInfo.CompSelectR)
    writer.WriteByte(HeaderInfo.CompSelectG)
    writer.WriteByte(HeaderInfo.CompSelectB)
    writer.WriteByte(HeaderInfo.CompSelectA)
    writer.WriteBytes(HeaderInfo.Hash)
    writer.WriteUInt16(HeaderInfo.Format)
    writer.WriteUInt16(HeaderInfo.Unknown3)
    writer.WriteUInt32(HeaderInfo.TextureSetting1)
    writer.WriteUInt32(HeaderInfo.TextureSetting2)
    writer.WriteUInt32(HeaderInfo.TextureSetting3)
    writer.WriteUInt32(HeaderInfo.TextureSetting4)

    writer.SeekBegin(HeaderInfo.HeaderSize)

    surfaceSizes = []
    surfaceData = []

    for mip in range(MipCount):
        for array in range(ArrayCount):
            writer.WriteUInt16(array)
            writer.WriteByte(mip)
            writer.WriteByte(1)

            surface = Zstb.SCompress(ImageList[array][mip], 20)
            surfaceSizes.append(len(surface))
            surfaceData.append(surface)

    for surface in surfaceSizes:
        writer.WriteUInt32(surface)
        writer.WriteUInt32(6)

    for data in surfaceData:
        writer.WriteBytes(data)

def Dispose():
    if FileName in PluginRuntime.TextureCache:
        del PluginRuntime.TextureCache[FileName]

def GetImageData(ArrayLevel=0, MipLevel=0, DepthLevel=0):
    data = ImageList[ArrayLevel][MipLevel]
    return TegraX1Swizzle.GetDirectImageData(self, data, MipLevel)

def SetImageData(bitmap, ArrayLevel):
    tex = TextureData()
    tex.Texture = Syroot.NintenTools.NSW.Bntx.Texture()
    tex.Format = Format
    tex.Width = Width
    tex.Height = Height
    tex.MipCount = MipCount
    tex.ArrayCount = ArrayCount
    tex.Texture.TextureData = [[]]

    tex.SetImageData(bitmap, ArrayLevel)
    SetImage(tex, ArrayLevel)

def Replace(FileName):
    tex = TextureData()
    tex.Replace(FileName, MipCount, 0, Format, Syroot.NintenTools.NSW.Bntx.GFX.SurfaceDim.Dim2D, 1)

    editor = LibraryGUI.GetActiveContent(ImageEditorBase)
    targetArray = 0
    if editor is not None:
        targetArray = editor.GetArrayDisplayLevel()

    SetImage(tex, targetArray)

def SetImage(tex, targetArray):
    if tex.Texture is None:
        return

    for i in range(len(ImageList[0])):
        print(f"SIZE 1 mip{i} {len(ImageList[0][i])}")

    if len(ImageList) > 1 and Format != tex.Format:
        raise Exception(f"Imported texture must use the original format for surface injecting! Expected {Format} but got {tex.Format}! If you need ASTC, use an astc encoder with .astc file format.")

    if len(tex.Texture.TextureData) == 1:
        ImageList[targetArray] = tex.Texture.TextureData[0]
    else:
        ImageList.clear()
        ImageList.extend(tex.Texture.TextureData)

    for i in range(len(ImageList[0])):
        print(f"SIZE 2 mip{i} {len(ImageList[0][i])}")

    Width = tex.Texture.Width
    Height = tex.Texture.Height
    MipCount = tex.Texture.MipCount
    ArrayCount = len(ImageList)
    Format = tex.Format

    IsEdited = True

    UpdateEditor()

    LoadOpenGLTexture()

def GetActiveContent(contentType):
    return None

def LoadEditor(editor):
    pass

def SaveFileFormat(txtg, FilePath):
    pass

def GetDirectImageData(txtg, data, MipLevel):
    return data

def open(filename):
    return Image()

def tobytes(self):
    return b""

def TXTG():
    return TXTG()

def FileType():
    return FileType()

def CanSave():
    return True

def Description():
    return ["Texture To Go"]

def Extension():
    return ["*.txtg"]

def FileName():
    return ""

def FilePath():
    return ""

def IFileInfo():
    return None

def Identify(stream):
    signature = stream.read(4)
    return signature == b"6PK0"

def Types():
    return []

def CanEdit():
    return True

def SupportedFormats():
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

def OnClick(treeview):
    UpdateEditor()

def UpdateEditor():
    editor = LibraryGUI.GetActiveContent(ImageEditorBase)
    if editor is None:
        editor = ImageEditorBase()
        editor.Dock = DockStyle.Fill
        LibraryGUI.LoadEditor(editor)

    prop = DisplayProperties()
    prop.Width = Width
    prop.Height = Height
    prop.MipCount = MipCount
    prop.ArrayCount = ArrayCount
    prop.Format = Format
    prop.Hash = "".join([format(x, "X2") for x in HeaderInfo.Hash])

    editor.Text = Text
    editor.LoadProperties(prop)
    editor.LoadImage(self)

def GetContextMenuItems():
    items = []
    items.append(ToolStripMenuItem("Save File", None, lambda o, e: STFileSaver.SaveFileFormat(self, FilePath)))
    items.extend(base.GetContextMenuItems())
    return items

def Load(stream):
    Tag = self

    CanReplace = True

    ImageKey = "Texture"
    SelectedImageKey = "Texture"

    name = os.path.splitext(os.path.basename(FileName))[0]
    Text = name

    if name in PluginRuntime.TextureCache:
        del PluginRuntime.TextureCache[name]
    PluginRuntime.TextureCache[name] = self

    reader = FileReader(stream, True)
    reader.SetByteOrder(False)

    HeaderInfo = Header()
    HeaderInfo.HeaderSize = reader.ReadUInt16()
    HeaderInfo.Version = reader.ReadUInt16()
    HeaderInfo.Magic = reader.ReadBytes(4)
    HeaderInfo.Width = reader.ReadUInt16()
    HeaderInfo.Height = reader.ReadUInt16()
    HeaderInfo.Depth = reader.ReadUInt16()
    HeaderInfo.MipCount = reader.ReadByte()
    HeaderInfo.Unknown1 = reader.ReadByte()
    HeaderInfo.Unknown2 = reader.ReadByte()
    HeaderInfo.Padding = reader.ReadUInt16()
    HeaderInfo.FormatFlag = reader.ReadByte()
    HeaderInfo.FormatSetting = reader.ReadUInt32()
    HeaderInfo.CompSelectR = reader.ReadByte()
    HeaderInfo.CompSelectG = reader.ReadByte()
    HeaderInfo.CompSelectB = reader.ReadByte()
    HeaderInfo.CompSelectA = reader.ReadByte()
    HeaderInfo.Hash = reader.ReadBytes(32)
    HeaderInfo.Format = reader.ReadUInt16()
    HeaderInfo.Unknown3 = reader.ReadUInt16()
    HeaderInfo.TextureSetting1 = reader.ReadUInt32()
    HeaderInfo.TextureSetting2 = reader.ReadUInt32()
    HeaderInfo.TextureSetting3 = reader.ReadUInt32()
    HeaderInfo.TextureSetting4 = reader.ReadUInt32()

    Width = HeaderInfo.Width
    Height = HeaderInfo.Height
    ArrayCount = HeaderInfo.Depth
    MipCount = HeaderInfo.MipCount

    RedChannel = ChannelList[HeaderInfo.CompSelectR]
    GreenChannel = ChannelList[HeaderInfo.CompSelectG]
    BlueChannel = ChannelList[HeaderInfo.CompSelectB]
    AlphaChannel = ChannelList[HeaderInfo.CompSelectA]

    surfaces = []
    reader.SeekBegin(HeaderInfo.HeaderSize)
    for i in range(MipCount * ArrayCount):
        surface = SurfaceInfo()
        surface.ArrayLevel = reader.ReadUInt16()
        surface.MipLevel = reader.ReadByte()
        reader.ReadByte()
        surfaces.append(surface)

    for i in range(MipCount * ArrayCount):
        surfaces[i].Size = reader.ReadUInt32()
        reader.ReadUInt32()

    pos = reader.Position

    if HeaderInfo.Format in FormatList:
        Format = FormatList[HeaderInfo.Format]
    else:
        raise Exception(f"Unsupported format! {HeaderInfo.Format:X}")

    data = []
    for i in range(MipCount * ArrayCount):
        imageData = reader.ReadBytes(surfaces[i].Size)
        if len(data) <= surfaces[i].ArrayLevel:
            data.append([])
        data[surfaces[i].ArrayLevel].append(Zstb.SDecompress(imageData))
    ImageList = data

def Save(stream):
    HeaderInfo.Format = next((k for k, v in FormatList.items() if v == Format), None)
    HeaderInfo.Width = Width
    HeaderInfo.Height = Height
    HeaderInfo.Depth = ArrayCount
    HeaderInfo.MipCount = MipCount

    writer = FileWriter(stream)
    writer.WriteUInt16(HeaderInfo.HeaderSize)
    writer.WriteUInt16(HeaderInfo.Version)
    writer.WriteBytes(HeaderInfo.Magic)
    writer.WriteUInt16(HeaderInfo.Width)
    writer.WriteUInt16(HeaderInfo.Height)
    writer.WriteUInt16(HeaderInfo.Depth)
    writer.WriteByte(HeaderInfo.MipCount)
    writer.WriteByte(HeaderInfo.Unknown1)
    writer.WriteByte(HeaderInfo.Unknown2)
    writer.WriteUInt16(HeaderInfo.Padding)
    writer.WriteByte(HeaderInfo.FormatFlag)
    writer.WriteUInt32(HeaderInfo.FormatSetting)
    writer.WriteByte(HeaderInfo.CompSelectR)
    writer.WriteByte(HeaderInfo.CompSelectG)
    writer.WriteByte(HeaderInfo.CompSelectB)
    writer.WriteByte(HeaderInfo.CompSelectA)
    writer.WriteBytes(HeaderInfo.Hash)
    writer.WriteUInt16(HeaderInfo.Format)
    writer.WriteUInt16(HeaderInfo.Unknown3)
    writer.WriteUInt32(HeaderInfo.TextureSetting1)
    writer.WriteUInt32(HeaderInfo.TextureSetting2)
    writer.WriteUInt32(HeaderInfo.TextureSetting3)
    writer.WriteUInt32(HeaderInfo.TextureSetting4)

    writer.SeekBegin(HeaderInfo.HeaderSize)

    surfaceSizes = []
    surfaceData = []

    for mip in range(MipCount):
        for array in range(ArrayCount):
            writer.WriteUInt16(array)
            writer.WriteByte(mip)
            writer.WriteByte(1)

            surface = Zstb.SCompress(ImageList[array][mip], 20)
            surfaceSizes.append(len(surface))
            surfaceData.append(surface)

    for surface in surfaceSizes:
        writer.WriteUInt32(surface)
        writer.WriteUInt32(6)

    for data in surfaceData:
        writer.WriteBytes(data)

def Dispose():
    if FileName in PluginRuntime.TextureCache:
        del PluginRuntime.TextureCache[FileName]

def GetImageData(ArrayLevel=0, MipLevel=0, DepthLevel=0):
    data = ImageList[ArrayLevel][MipLevel]
    return TegraX1Swizzle.GetDirectImageData(self, data, MipLevel)

def SetImageData(bitmap, ArrayLevel):
    tex = TextureData()
    tex.Texture = Syroot.NintenTools.NSW.Bntx.Texture()
    tex.Format = Format
    tex.Width = Width
    tex.Height = Height
    tex.MipCount = MipCount
    tex.ArrayCount = ArrayCount
    tex.Texture.TextureData = [[]]

    tex.SetImageData(bitmap, ArrayLevel)
    SetImage(tex, ArrayLevel)

def Replace(FileName):
    tex = TextureData()
    tex.Replace(FileName, MipCount, 0, Format, Syroot.NintenTools.NSW.Bntx.GFX.SurfaceDim.Dim2D, 1)

    editor = LibraryGUI.GetActiveContent(ImageEditorBase)
    targetArray = 0
    if editor is not None:
        targetArray = editor.GetArrayDisplayLevel()

    SetImage(tex, targetArray)

def SetImage(tex, targetArray):
    if tex.Texture is None:
        return

    for i in range(len(ImageList[0])):
        print(f"SIZE 1 mip{i} {len(ImageList[0][i])}")

    if len(ImageList) > 1 and Format != tex.Format:
        raise Exception(f"Imported texture must use the original format for surface injecting! Expected {Format} but got {tex.Format}! If you need ASTC, use an astc encoder with .astc file format.")

    if len(tex.Texture.TextureData) == 1:
        ImageList[targetArray] = tex.Texture.TextureData[0]
    else:
        ImageList.clear()
        ImageList.extend(tex.Texture.TextureData)

    for i in range(len(ImageList[0])):
        print(f"SIZE 2 mip{i} {len(ImageList[0][i])}")

    Width = tex.Texture.Width
    Height = tex.Texture.Height
    MipCount = tex.Texture.MipCount
    ArrayCount = len(ImageList)
    Format = tex.Format

    IsEdited = True

    UpdateEditor()

    LoadOpenGLTexture()

def GetActiveContent(contentType):
    return None

def LoadEditor(editor):
    pass

def SaveFileFormat(txtg, FilePath):
    pass

def GetDirectImageData(txtg, data, MipLevel):
    return data

def open(filename):
    return Image()

def tobytes(self):
    return b""

def TXTG():
    return TXTG()

def FileType():
    return FileType()

def CanSave():
    return True

def Description():
    return ["Texture To Go"]

def Extension():
    return ["*.txtg"]

def FileName():
    return ""

def FilePath():
    return ""

def IFileInfo():
    return None

def Identify(stream):
    signature = stream.read(4)
    return signature == b"6PK0"

def Types():
    return []

def CanEdit():
    return True

def SupportedFormats():
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

def OnClick(treeview):
    UpdateEditor()

def UpdateEditor():
    editor = LibraryGUI.GetActiveContent(ImageEditorBase)
    if editor is None:
        editor = ImageEditorBase()
        editor.Dock = DockStyle.Fill
        LibraryGUI.LoadEditor(editor)

    prop = DisplayProperties()
    prop.Width = Width
    prop.Height = Height
    prop.MipCount = MipCount
    prop.ArrayCount = ArrayCount
    prop.Format = Format
    prop.Hash = "".join([format(x, "X2") for x in HeaderInfo.Hash])

    editor.Text = Text
    editor.LoadProperties(prop)
    editor.LoadImage(self)

def GetContextMenuItems():
    items = []
    items.append(ToolStripMenuItem("Save File", None, lambda o, e: STFileSaver.SaveFileFormat(self, FilePath)))
    items.extend(base.GetContextMenuItems())
    return items

def Load(stream):
    Tag = self

    CanReplace = True

    ImageKey = "Texture"
    SelectedImageKey = "Texture"

    name = os.path.splitext(os.path.basename(FileName))[0]
    Text = name

    if name in PluginRuntime.TextureCache:
        del PluginRuntime.TextureCache[name]
    PluginRuntime.TextureCache[name] = self

    reader = FileReader(stream, True)
    reader.SetByteOrder(False)

    HeaderInfo = Header()
    HeaderInfo.HeaderSize = reader.ReadUInt16()
    HeaderInfo.Version = reader.ReadUInt16()
    HeaderInfo.Magic = reader.ReadBytes(4)
    HeaderInfo.Width = reader.ReadUInt16()
    HeaderInfo.Height = reader.ReadUInt16()
    HeaderInfo.Depth = reader.ReadUInt16()
    HeaderInfo.MipCount = reader.ReadByte()
    HeaderInfo.Unknown1 = reader.ReadByte()
    HeaderInfo.Unknown2 = reader.ReadByte()
    HeaderInfo.Padding = reader.ReadUInt16()
    HeaderInfo.FormatFlag = reader.ReadByte()
    HeaderInfo.FormatSetting = reader.ReadUInt32()
    HeaderInfo.CompSelectR = reader.ReadByte()
    HeaderInfo.CompSelectG = reader.ReadByte()
    HeaderInfo.CompSelectB = reader.ReadByte()
    HeaderInfo.CompSelectA = reader.ReadByte()
    HeaderInfo.Hash = reader.ReadBytes(32)
    HeaderInfo.Format = reader.ReadUInt16()
    HeaderInfo.Unknown3 = reader.ReadUInt16()
    HeaderInfo.TextureSetting1 = reader.ReadUInt32()
    HeaderInfo.TextureSetting2 = reader.ReadUInt32()
    HeaderInfo.TextureSetting3 = reader.ReadUInt32()
    HeaderInfo.TextureSetting4 = reader.ReadUInt32()

    Width = HeaderInfo.Width
    Height = HeaderInfo.Height
    ArrayCount = HeaderInfo.Depth
    MipCount = HeaderInfo.MipCount

    RedChannel = ChannelList[HeaderInfo.CompSelectR]
    GreenChannel = ChannelList[HeaderInfo.CompSelectG]
    BlueChannel = ChannelList[HeaderInfo.CompSelectB]
    AlphaChannel = ChannelList[HeaderInfo.CompSelectA]

    surfaces = []
    reader.SeekBegin(HeaderInfo.HeaderSize)
    for i in range(MipCount * ArrayCount):
        surface = SurfaceInfo()
        surface.ArrayLevel = reader.ReadUInt16()
        surface.MipLevel = reader.ReadByte()
        reader.ReadByte()
        surfaces.append(surface)

    for i in range(MipCount * ArrayCount):
        surfaces[i].Size = reader.ReadUInt32()
        reader.ReadUInt32()

    pos = reader.Position

    if HeaderInfo.Format in FormatList:
        Format = FormatList[HeaderInfo.Format]
    else:
        raise Exception(f"Unsupported format! {HeaderInfo.Format:X}")

    data = []
    for i in range(MipCount * ArrayCount):
        imageData = reader.ReadBytes(surfaces[i].Size)
        if len(data) <= surfaces[i].ArrayLevel:
            data.append([])
        data[surfaces[i].ArrayLevel].append(Zstb.SDecompress(imageData))
    ImageList = data

def Save(stream):
    HeaderInfo.Format = next((k for k, v in FormatList.items() if v == Format), None)
    HeaderInfo.Width = Width
    HeaderInfo.Height = Height
    HeaderInfo.Depth = ArrayCount
    HeaderInfo.MipCount = MipCount

    writer = FileWriter(stream)
    writer.WriteUInt16(HeaderInfo.HeaderSize)
    writer.WriteUInt16(HeaderInfo.Version)
    writer.WriteBytes(HeaderInfo.Magic)
    writer.WriteUInt16(HeaderInfo.Width)
    writer.WriteUInt16(HeaderInfo.Height)
    writer.WriteUInt16(HeaderInfo.Depth)
    writer.WriteByte(HeaderInfo.MipCount)
    writer.WriteByte(HeaderInfo.Unknown1)
    writer.WriteByte(HeaderInfo.Unknown2)
    writer.WriteUInt16(HeaderInfo.Padding)
    writer.WriteByte(HeaderInfo.FormatFlag)
    writer.WriteUInt32(HeaderInfo.FormatSetting)
    writer.WriteByte(HeaderInfo.CompSelectR)
    writer.WriteByte(HeaderInfo.CompSelectG)
    writer.WriteByte(HeaderInfo.CompSelectB)
    writer.WriteByte(HeaderInfo.CompSelectA)
    writer.WriteBytes(HeaderInfo.Hash)
    writer.WriteUInt16(HeaderInfo.Format)
    writer.WriteUInt16(HeaderInfo.Unknown3)
    writer.WriteUInt32(HeaderInfo.TextureSetting1)
    writer.WriteUInt32(HeaderInfo.TextureSetting2)
    writer.WriteUInt32(HeaderInfo.TextureSetting3)
    writer.WriteUInt32(HeaderInfo.TextureSetting4)

    writer.SeekBegin(HeaderInfo.HeaderSize)

    surfaceSizes = []
    surfaceData = []

    for mip in range(MipCount):
        for array in range(ArrayCount):
            writer.WriteUInt16(array)
            writer.WriteByte(mip)
            writer.WriteByte(1)

            surface = Zstb.SCompress(ImageList[array][mip], 20)
            surfaceSizes.append(len(surface))
            surfaceData.append(surface)

    for surface in surfaceSizes:
        writer.WriteUInt32(surface)
        writer.WriteUInt32(6)

    for data in surfaceData:
        writer.WriteBytes(data)

def Dispose():
    if FileName in PluginRuntime.TextureCache:
        del PluginRuntime.TextureCache[FileName]

def GetImageData(ArrayLevel=0, MipLevel=0, DepthLevel=0):
    data = ImageList[ArrayLevel][MipLevel]
    return TegraX1Swizzle.GetDirectImageData(self, data, MipLevel)

def SetImageData(bitmap, ArrayLevel):
    tex = TextureData()
    tex.Texture = Syroot.NintenTools.NSW.Bntx.Texture()
    tex.Format = Format
    tex.Width = Width
    tex.Height = Height
    tex.MipCount = MipCount
    tex.ArrayCount = ArrayCount
    tex.Texture.TextureData = [[]]

    tex.SetImageData(bitmap, ArrayLevel)
    SetImage(tex, ArrayLevel)

def Replace(FileName):
    tex = TextureData()
    tex.Replace(FileName, MipCount, 0, Format, Syroot.NintenTools.NSW.Bntx.GFX.SurfaceDim.Dim2D, 1)

    editor = LibraryGUI.GetActiveContent(ImageEditorBase)
    targetArray = 0
    if editor is not None:
        targetArray = editor.GetArrayDisplayLevel()

    SetImage(tex, targetArray)

def SetImage(tex, targetArray):
    if tex.Texture is None:
        return

    for i in range(len(ImageList[0])):
        print(f"SIZE 1 mip{i} {len(ImageList[0][i])}")

    if len(ImageList) > 1 and Format != tex.Format:
        raise Exception(f"Imported texture must use the original format for surface injecting! Expected {Format} but got {tex.Format}! If you need ASTC, use an astc encoder with .astc file format.")

    if len(tex.Texture.TextureData) == 1:
        ImageList[targetArray] = tex.Texture.TextureData[0]
    else:
        ImageList.clear()
        ImageList.extend(tex.Texture.TextureData)

    for i in range(len(ImageList[0])):
        print(f"SIZE 2 mip{i} {len(ImageList[0][i])}")

    Width = tex.Texture.Width
    Height = tex.Texture.Height
    MipCount = tex.Texture.MipCount
    ArrayCount = len(ImageList)
    Format = tex.Format

    IsEdited = True

    UpdateEditor()

    LoadOpenGLTexture()

def GetActiveContent(contentType):
    return None

def LoadEditor(editor):
    pass

def SaveFileFormat(txtg, FilePath):
    pass

def GetDirectImageData(txtg, data, MipLevel):
    return data

def open(filename):
    return Image()

def tobytes(self):
    return b""

def TXTG():
    return TXTG()

def FileType():
    return FileType()

def CanSave():
    return True

def Description():
    return ["Texture To Go"]

def Extension():
    return ["*.txtg"]

def FileName():
    return ""

def FilePath():
    return ""

def IFileInfo():
    return None

def Identify(stream):
    signature = stream.read(4)
    return signature == b"6PK0"

def Types():
    return []

def CanEdit():
    return True

def SupportedFormats():
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

def OnClick(treeview):
    UpdateEditor()

def UpdateEditor():
    editor = LibraryGUI.GetActiveContent(ImageEditorBase)
    if editor is None:
        editor = ImageEditorBase()
        editor.Dock = DockStyle.Fill
        LibraryGUI.LoadEditor(editor)

    prop = DisplayProperties()
    prop.Width = Width
    prop.Height = Height
    prop.MipCount = MipCount
    prop.ArrayCount = ArrayCount
    prop.Format = Format
    prop.Hash = "".join([format(x, "X2") for x in HeaderInfo.Hash])

    editor.Text = Text
    editor.LoadProperties(prop)
    editor.LoadImage(self)

def GetContextMenuItems():
    items = []
    items.append(ToolStripMenuItem("Save File", None, lambda o, e: STFileSaver.SaveFileFormat(self, FilePath)))
    items.extend(base.GetContextMenuItems())
    return items

def Load(stream):
    Tag = self

    CanReplace = True

    ImageKey = "Texture"
    SelectedImageKey = "Texture"

    name = os.path.splitext(os.path.basename(FileName))[0]
    Text = name

    if name in PluginRuntime.TextureCache:
        del PluginRuntime.TextureCache[name]
    PluginRuntime.TextureCache[name] = self

    reader = FileReader(stream, True)
    reader.SetByteOrder(False)

    HeaderInfo = Header()
    HeaderInfo.HeaderSize = reader.ReadUInt16()
    HeaderInfo.Version = reader.ReadUInt

