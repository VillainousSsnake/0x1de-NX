# Largely adapated from https://github.com/zeldamods/evfl
import struct
import io
import tempfile

import mmh3
import binascii


class Stream:
    __slots__ = ["stream"]

    def __init__(self, stream) -> None:
        self.stream = stream

    def seek(self, *args) -> None:
        self.stream.seek(*args)

    def tell(self) -> int:
        return self.stream.tell()

    def skip(self, skip_size) -> None:
        self.stream.seek(skip_size, 1)


class ReadStream(Stream):
    def __init__(self, data) -> None:
        stream = io.BytesIO(memoryview(data))
        super().__init__(stream)
        self.data = data

    def read(self, *args) -> bytes:
        return self.stream.read(*args)

    def read_u8(self, end="<") -> int:
        return struct.unpack(f"{end}B", self.read(1))[0]

    def read_u16(self, end="<") -> int:
        return struct.unpack(f"{end}H", self.read(2))[0]

    def read_s16(self, end="<") -> int:
        return struct.unpack(f"{end}h", self.read(2))[0]

    def read_u24(self, end="<") -> int:
        if end == "<":
            return struct.unpack(f"{end}I", self.read(3) + b'\x00')[0]
        else:
            return struct.unpack(f"{end}I", b'\x00' + self.read(3))[0]

    def read_s24(self, end="<") -> int:
        if end == "<":
            return struct.unpack(f"{end}i", self.read(3) + b'\x00')[0]
        else:
            return struct.unpack(f"{end}i", b'\x00' + self.read(3))[0]

    def read_u32(self, end="<") -> int:
        return struct.unpack(f"{end}I", self.read(4))[0]

    def read_s32(self, end="<") -> int:
        return struct.unpack(f"{end}i", self.read(4))[0]

    def read_u64(self, end="<") -> int:
        return struct.unpack(f"{end}Q", self.read(8))[0]

    def read_s64(self, end="<") -> int:
        return struct.unpack(f"{end}q", self.read(8))[0]

    def read_ptr(self, align=8, end="<") -> int:
        while self.stream.tell() % align != 0:
            self.read(1)
        return struct.unpack(f"{end}Q", self.read(8))[0]

    def read_f32(self, end="<") -> float:
        return struct.unpack(f"{end}f", self.read(4))[0]

    def read_f64(self, end="<") -> float:
        return struct.unpack(f"{end}d", self.read(4))[0]

    def read_string(self):
        string = b''
        current_char = self.stream.read(1)
        while current_char != b'\x00':
            string += current_char
            current_char = self.stream.read(1)
        return string.decode('utf-8')

    def read_string_pool(self, offset, string_pool_offset, end="<"):
        pos = self.stream.tell()
        self.stream.seek(string_pool_offset + offset)
        data = self.read()
        end = data.find(b'\x00')
        string = data[offset:end].decode('utf-8')
        self.stream.seek(pos)
        return string


class WriteStream(Stream):
    def __init__(self, stream):
        super().__init__(stream)
        self._string_list = []  # List of strings in file
        self._strings = b''  # String pool to write to file
        self._string_refs = {}  # Maps strings to relative offsets
        self._string_list_exb = []  # List of strings in the EXB Section
        self._strings_exb = b''  # String pool to write to the EXB section
        self._string_refs_exb = {}  # Maps strings to relative offsets

    def add_string(self, string):
        if string not in self._string_list:
            encoded = string.encode()
            self._string_list.append(string)
            self._string_refs[string] = len(self._strings)
            self._strings += encoded
            if encoded[-1:] != b'\x00':  # All strings must end with a null termination character
                self._strings += b'\x00'

    def add_string_exb(self, string):
        if string not in self._string_list_exb:
            encoded = string.encode()
            self._string_list_exb.append(string)
            self._string_refs_exb[string] = len(self._strings_exb)
            self._strings_exb += encoded
            if encoded[-1:] != b'\x00':  # All strings must end with a null termination character
                self._strings_exb += b'\x00'

    def align_up(self, alignment):
        while self.stream.tell() % alignment != 0:
            self.skip(1)

    def write(self, data):
        self.stream.write(data)

    def read(self, *args):
        self.stream.read(*args)


def u8(value):
    return struct.pack("<B", value)


def s8(value):
    return struct.pack("<b", value)


def u16(value, end="<"):
    return struct.pack(f"{end}H", value)


def s16(value, end="<"):
    return struct.pack(f"{end}h", value)


def u24(value, end="<"):
    ret = struct.pack(f"{end}I", value)
    return ret[1:] if end == ">" else ret[:-1]


def s24(value, end="<"):
    ret = struct.pack(f"{end}i", value)
    return ret[1:] if end == ">" else ret[:-1]


def u32(value, end="<"):
    return struct.pack(f"{end}I", value)


def s32(value, end="<"):
    return struct.pack(f"{end}i", value)


def u64(value, end="<"):
    return struct.pack(f"{end}Q", value)


def s64(value, end="<"):
    return struct.pack(f"{end}q", value)


def f32(value, end="<"):
    return struct.pack(f"{end}f", value)


def f64(value, end="<"):
    return struct.pack(f"{end}d", value)


def byte_custom(value, size, end="<"):
    return struct.pack(f"{end}{size}s", value)


def string(value):
    return value.encode('utf-8')


def vec3f(values, end="<"):
    ret = b''
    for value in values:
        ret += f32(value, end)
    return ret


def padding(count):
    return struct.pack(f"{count}s", b'\x00')


def hash(value):
    return mmh3.hash(value, signed=False)


def crc32(value):
    return binascii.crc32(value)

                                                                # TODO: DOWN IS THE BYML LIB
import os
import json

try:
    import yaml
except ImportError:
    raise ImportError("Would you be so kind as to LEARN TO FUCKING READ INSTRUCTIONS")

"""
Node Types:
HashArray(1-16)         = 0x20->0x2F
HashArrayWithRemap(1-16)= 0x30->0x3F
StringIndex             = 0xA0
BinaryData              = 0xA1
BinaryDataWithAlignment = 0xA2
Array                   = 0xC0
Dictionary              = 0xC1
StringTable             = 0xC2
DictionaryWithRemap     = 0xC4
RelocatedStringTable    = 0xC5
MonoTypedArray          = 0xC8
Bool                    = 0xD0
Int                     = 0xD1
Float                   = 0xD2
UInt                    = 0xD3
Long                    = 0xD4
ULong                   = 0xD5
Double                  = 0xD6
Null                    = 0xFF
"""


class Int(int):
    pass


class Float(float):
    pass


class UInt(int):
    pass


class Long(int):
    pass


class ULong(int):
    pass


class Double(float):
    pass


# From zeldamods byml-v2 library
def add_representers(dumper):
    yaml.add_representer(Int, lambda d, data: d.represent_int(data), Dumper=dumper)
    yaml.add_representer(Float, lambda d, data: d.represent_float(data), Dumper=dumper)
    yaml.add_representer(UInt, lambda d, data: d.represent_scalar(u'!u', str(data)), Dumper=dumper)
    yaml.add_representer(Long, lambda d, data: d.represent_scalar(u'!l', str(data)), Dumper=dumper)
    yaml.add_representer(ULong, lambda d, data: d.represent_scalar(u'!ul', str(data)), Dumper=dumper)
    yaml.add_representer(Double, lambda d, data: d.represent_scalar(u'!f64', str(data)), Dumper=dumper)


def add_constructors(loader):
    yaml.add_constructor(u'tag:yaml.org,2002:int', lambda l, node: Int(l.construct_yaml_int(node)), Loader=loader)
    yaml.add_constructor(u'tag:yaml.org,2002:float', lambda l, node: Float(l.construct_yaml_float(node)), Loader=loader)
    yaml.add_constructor(u'!u', lambda l, node: UInt(l.construct_yaml_int(node)), Loader=loader)
    yaml.add_constructor(u'!l', lambda l, node: Long(l.construct_yaml_int(node)), Loader=loader)
    yaml.add_constructor(u'!ul', lambda l, node: ULong(l.construct_yaml_int(node)), Loader=loader)
    yaml.add_constructor(u'!f64', lambda l, node: Double(l.construct_yaml_float(node)), Loader=loader)


class Byml:
    def __init__(self, data, filename=''):
        if type(data) != bytes:
            self.filename = os.path.basename(data)
            if os.path.splitext(self.filename)[1] in ['.yml', '.yaml']:
                with open(data, 'r', encoding='utf-8') as file:
                    loader = yaml.SafeLoader
                    add_constructors(loader)
                    self.root_node = yaml.load(file, Loader=loader)
                    self.magic = 'YB'
                    self.version = 7
                    return
            elif os.path.splitext(self.filename)[1] in ['.byml', '.byaml', '.bgyml']:
                with open(data, 'rb') as file:
                    data = file.read()
        else:
            self.filename = filename

        self.stream = ReadStream(data)

        self.magic = self.stream.read(2).decode('utf-8')
        if self.magic not in ['BY', 'YB']:
            raise ValueError(f"Invalid file magic, expected 'BY' or 'YB' but got {self.magic}")
        if self.magic == 'BY':
            self.bom = ">"
        elif self.magic == 'YB':
            self.bom = "<"
        self.version = self.stream.read_u16(self.bom)
        if self.version > 0x7:
            raise ValueError(f"Only versions <=7 are supported, got version {self.version}")
        self.key_table_offset = self.stream.read_u32(self.bom)  # String table of key names
        self.string_table_offset = self.stream.read_u32(self.bom)  # String table of string values
        self.root_node_offset = self.stream.read_u32(self.bom)  # Root node must be a hash array, array, or dictionary

        if self.key_table_offset:
            self.stream.seek(self.key_table_offset)
            self.key_table = self.ParseNode()
        else:
            self.key_table = []
        if self.string_table_offset:
            self.stream.seek(self.string_table_offset)
            self.string_table = self.ParseNode()
        else:
            self.string_table = []
        if self.root_node_offset:
            self.stream.seek(self.root_node_offset)
            self.root_node = self.ParseNode()
        else:
            self.root_node = {}

    def ToYaml(self) -> str:
        temp_dir = tempfile.TemporaryDirectory()
        out_file = os.path.join(temp_dir.name, "output.yml")

        dumper = yaml.Dumper
        add_representers(dumper)

        with open(out_file, 'w') as f_out:
            yaml.dump(self.root_node, f_out, sort_keys=False, allow_unicode=True, Dumper=dumper)

        with open(out_file, "r") as f_in:
            return f_in.read()

    def ToJson(self) -> str:
        temp_dir = tempfile.TemporaryDirectory()
        out_file = os.path.join(temp_dir.name, "output.json")

        with open(out_file, 'w') as f_out:
            json.dump(self.root_node, f_out, indent=4)

        with open(out_file, 'r') as f_in:
            return f_in.read()

    # lazy reserialization for now, hopefully will work on getting all node types for later
    def Reserialize(self, output_dir=''):
        with open(os.path.join(output_dir, self.filename), 'wb+') as f:
            buffer = WriteStream(f)
            buffer.write(self.magic.encode())
            buffer.write(u16(self.version, self.bom))
            buffer.skip(12)
            self.key_table, self.string_table = [], []
            self.GenerateStringTables(self.root_node)
            key_table_offset = buffer.tell()
            self.key_table.sort()
            self.WriteStringTable(self.key_table, buffer)
            string_table_offset = buffer.tell()
            self.string_table.sort()
            self.WriteStringTable(self.string_table, buffer)
            root_node_offset = buffer.tell()
            nodes = {}
            self.WriteNode(self.root_node, nodes, buffer)

            buffer.seek(4)
            buffer.write(u32(key_table_offset, self.bom))
            buffer.write(u32(string_table_offset, self.bom))
            buffer.write(u32(root_node_offset, self.bom))

    def WriteNode(self, node, nodes, buffer):
        nonvalue_nodes = []

        if isinstance(node, list):
            buffer.write(u8(0xC0))
            buffer.write(u24(len(node), self.bom))
            for item in node:
                buffer.write(u8(self.GetNodeType(item)))
            buffer.align_up(4)
            for item in node:
                if self.IsValue(item):
                    buffer.write(self.FormatValue(item, self.string_table, self.bom))
                else:
                    nonvalue_nodes.append((item, buffer.tell()))
                    buffer.write(u32(0))
        elif isinstance(node, dict):
            # remind myself to check for uint keys from hash arrays
            buffer.write(u8(0xC1))
            buffer.write(u24(len(node), self.bom))
            for key in sorted(node.keys()):
                value = node[key]
                buffer.write(u24(self.key_table.index(key), self.bom))
                buffer.write(u8(self.GetNodeType(value)))
                if self.IsValue(value):
                    buffer.write(self.FormatValue(value, self.string_table, self.bom))
                else:
                    nonvalue_nodes.append((value, buffer.tell()))
                    buffer.write(u32(0))
        elif isinstance(node, bytes):
            buffer.write(u32(len(node), self.bom))
            buffer.write(node)
        elif isinstance(node, Long):
            buffer.write(s64(node, self.bom))
        elif isinstance(node, ULong):
            buffer.write(u64(node, self.bom))
        elif isinstance(node, Double):
            buffer.write(f64(node, self.bom))
        else:
            raise ValueError(f"Invalid/unsupported node data: {type(node)}")

        buffer.align_up(4)

        for (data, offset) in nonvalue_nodes:
            node_data = data
            data = (self.GetNodeType(data), self.FreezeObj(data))
            if data in nodes:
                pos = buffer.tell()
                buffer.seek(offset)
                buffer.write(u32(nodes[data], self.bom))
                buffer.seek(pos)
            else:
                pos = buffer.tell()
                address = buffer.tell()
                buffer.seek(offset)
                buffer.write(u32(address, self.bom))
                nodes[data] = address
                buffer.seek(pos)
                self.WriteNode(node_data, nodes, buffer)

    def WriteStringTable(self, table, buffer):
        start = buffer.tell()
        buffer.write(u8(0xC2))
        buffer.write(u24(len(table), self.bom))
        offsets = []
        buffer.skip(4 * len(table) + 4)
        for entry in table:
            offsets.append(buffer.tell() - start)
            buffer.write(entry.encode('utf-8') + b'\x00')
        end = buffer.tell()
        offsets.append(end - start)
        buffer.seek(start + 4)
        for offset in offsets:
            buffer.write(u32(offset, self.bom))
        buffer.seek(end)
        buffer.align_up(4)

    def ParseNode(self):
        node_info = self.GetContainerInfo()
        return self.GetValue(node_info)

    def GetContainerInfo(self):
        return (self.stream.read_u8(), self.stream.read_u24(self.bom))

    def GetValue(self, node_info):
        if node_info[0] >= 0x20 and node_info[0] <= 0x2f:
            return self.HashArray(node_info)
        elif node_info[0] >= 0x30 and node_info[0] <= 0x3f:
            return self.HashArrayWithRemap(node_info)
        elif node_info[0] == 0xa0:
            return self.StringIndex(node_info)
        elif node_info[0] == 0xa1:
            return self.BinaryData(node_info)
        elif node_info[0] == 0xa2:
            return self.BinaryDataWithAlignment(node_info)
        elif node_info[0] == 0xc0:
            return self.Array(node_info)
        elif node_info[0] == 0xc1:
            return self.Dictionary(node_info)
        elif node_info[0] == 0xc2:
            return self.StringTable(node_info)
        elif node_info[0] == 0xc4:
            return self.DictionaryWithRemap(node_info)
        elif node_info[0] == 0xc5:
            return self.MonoTypedArray(node_info)
        elif node_info[0] == 0xd0:
            return bool(self.stream.read_u32(self.bom))
        elif node_info[0] == 0xd1:
            return Int(self.stream.read_s32(self.bom))
        elif node_info[0] == 0xd2:
            return Float(self.stream.read_f32(self.bom))
        elif node_info[0] == 0xd3:
            return UInt(self.stream.read_u32(self.bom))
        elif node_info[0] == 0xd4:
            return Long(self.stream.read_s64(self.bom))
        elif node_info[0] == 0xd5:
            return ULong(self.stream.read_u64(self.bom))
        elif node_info[0] == 0xd6:
            return Double(self.stream.read_f64(self.bom))
        elif node_info[0] == 0xff:
            return
        else:
            raise ValueError(
                f"Invalid node type: {hex(node_info[0])}\nFile: {self.filename}\nOffset: {hex(self.stream.tell())}")

    def GetArrayValue(self, node_info):
        if node_info[0] < 0xa0 or node_info[0] in [0xc0, 0xc1, 0xc4, 0xc8]:
            pos = self.stream.tell() + 4
            self.stream.seek(self.stream.read_u32(self.bom))
            node = self.ParseNode()
            self.stream.seek(pos)
            return node
        elif node_info[0] in [0xa1, 0xa2, 0xd4, 0xd5, 0xd6]:
            pos = self.stream.tell() + 4
            self.stream.seek(self.stream.read_u32(self.bom))
            node = self.GetValue(node_info)
            self.stream.seek(pos)
            return node
        else:
            return self.GetValue(node_info)

    def HashArray(self, node_info):
        entry_size = ((node_info[0] & 0xf) + 1) * 0x4 + 0x4
        pos = self.stream.tell()
        self.stream.read(entry_size * node_info[1])
        types = []
        for i in range(node_info[1]):
            types.append(self.stream.read_u8())
        self.stream.seek(pos)
        entries = []
        for i in range(node_info[1]):
            entry = {}
            hash = self.stream.read(4 * ((node_info[0] & 0xf) + 1)).hex()
            entry[hash] = self.GetArrayValue((types[i], 1))
            entries.append(entry)
        return entries

    # Unsupported
    def HashArrayWithRemap(self, node_info):
        pass

    def StringIndex(self, node_info):
        return self.string_table[self.stream.read_u32(self.bom)]

    def BinaryData(self, node_info):
        size = self.stream.read_u32(self.bom)
        return self.stream.read(size)

    def BinaryDataWithAlignment(self, node_info):
        size = self.stream.read_u32(self.bom)
        align = self.stream.read_u32(self.bom)
        while self.stream.tell() % align != 0:
            self.stream.read(1)
        return self.stream.read(size)

    def Array(self, node_info):
        types = []
        for i in range(node_info[1]):
            types.append(self.stream.read_u8())
        while self.stream.tell() % 4 != 0:
            self.stream.read(1)
        entries = []
        for i in range(node_info[1]):
            entries.append(self.GetArrayValue((types[i], 1)))
        return entries

    def Dictionary(self, node_info):
        entries = {}
        for i in range(node_info[1]):
            name_index = self.stream.read_u24(self.bom)
            node_type = self.stream.read_u8()
            entries[self.key_table[name_index]] = self.GetArrayValue((node_type, 1))
        return entries

    def StringTable(self, node_info):
        base_offsets = self.stream.tell() - 4
        offsets = []
        for i in range(node_info[1]):
            offsets.append(self.stream.read_u32(self.bom))
        strings = []
        for i in range(node_info[1]):
            self.stream.seek(base_offsets + offsets[i])
            strings.append(self.stream.read_string())
        return strings

    # Unsupported
    def DictionaryWithRemap(self, node_info):
        pass

    # Unsupported
    def RelocatedStringTable(self, node_info):
        pass

    def MonoTypedArray(self, node_info):
        array_type = self.stream.read_u8()
        self.stream.read(3)
        entries = []
        for i in range(node_info[1]):
            entries.append(self.GetArrayValue((array_type, 1)))
        return entries

    # essentially pulled from byml library
    def GenerateStringTables(self, data):
        if type(data) == str and data not in self.string_table:
            self.string_table.append(data)
        elif type(data) == list:
            for item in data:
                self.GenerateStringTables(item)
        elif type(data) == dict:
            for k in data:
                if k not in self.key_table:
                    self.key_table.append(k)
                self.GenerateStringTables(data[k])

    # from the byml library for now, should probably expand for all node types eventually
    @staticmethod
    def GetNodeType(data):
        if isinstance(data, str):
            return 0xA0
        if isinstance(data, bytes):
            return 0xA1
        if isinstance(data, list):
            return 0xC0
        if isinstance(data, dict):
            return 0xC1
        if isinstance(data, bool):
            return 0xD0
        if isinstance(data, Int):
            return 0xD1
        if isinstance(data, Float):
            return 0xD2
        if isinstance(data, UInt):
            return 0xD3
        if isinstance(data, Long):
            return 0xD4
        if isinstance(data, ULong):
            return 0xD5
        if isinstance(data, Double):
            return 0xD6
        if data is None:
            return 0xFF
        raise ValueError(f"Invalid data type: {type(data)}")

    @staticmethod
    def IsValue(data):
        if type(data) in [str, bool, Int, Float, UInt] or data is None:
            return True
        return False

    @staticmethod
    def FormatValue(data, string_table, bom):
        if isinstance(data, str):
            return u32(string_table.index(data), bom)
        if isinstance(data, bool):
            return u32(1 if data else 0, bom)
        if isinstance(data, Int):
            return s32(data, bom)
        if isinstance(data, Float):
            return f32(data, bom)
        if isinstance(data, UInt):
            return u32(data, bom)
        if data is None:
            return u32(0, bom)
        raise ValueError(f"Invalid value type: {type(data)}")

    @staticmethod
    def FreezeObj(o):
        def Freeze(o):
            if isinstance(o, dict):
                return frozenset({k: Freeze(v) for k, v in o.items()}.items())
            if isinstance(o, list):
                return tuple([Freeze(i) for i in o])
            return str(o) + str(type(o))

        return Freeze(o)


def ExtractPtcl(path_to_esetb):
    filepath = path_to_esetb
    files = os.listdir(filepath)
    if not (os.path.exists('ptcl')):
        os.makedirs('ptcl')
    for file in files:
        print(file)
        byml = Byml(os.path.join(filepath, file))
        if 'PtclBin' in byml.root_node:
            with open('ptcl/' + os.path.splitext(byml.filename)[0] + '.ptcl', 'wb') as f:
                f.write(byml.root_node['PtclBin'])