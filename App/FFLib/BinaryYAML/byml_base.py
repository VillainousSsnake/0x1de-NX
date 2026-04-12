# Largely adapated from https://github.com/zeldamods/evfl
import struct
from io import BytesIO
import io
import tempfile
import zlib
import yaml
from collections import OrderedDict
from typing import Any, Dict, List, Tuple
import mmh3
import binascii

import yaml
from collections import OrderedDict


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

    # todo: lazy reserialization for now, hopefully will work on getting all node types for later
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


# Node type constants
NODE_ARRAY = 0xC0
NODE_STRING_TABLE = 0xC2
NODE_HASH = 0x20
NODE_BINARY = 0xA1
# New constant
NODE_STRING_HASH = 0xC1

# Primitive value type markers (we will encode the 4-byte "value" with a leading type byte)
VAL_NULL = 0xFF
VAL_BOOL = 0xD0
VAL_INT = 0xD1
VAL_FLOAT = 0xD2
VAL_UINT = 0xD3
VAL_STRING_INDEX = 0xA0


def hash_key(s: str) -> int:
    """32-bit hash for keys (CRC32)."""
    return zlib.crc32(s.encode('utf-8')) & 0xFFFFFFFF

def align4(n: int) -> int:
    return (n + 3) & ~3

class BYMLBuilder:
    def __init__(self, endian: str = '<'):
        """
        endian: '<' for little-endian (YB), '>' for big-endian (BY)
        """
        assert endian in ('<', '>')
        self.endian = endian
        self.strings: List[str] = []
        self.string_index: Dict[str, int] = {}
        self.nodes: List[Tuple[int, bytes]] = []  # list of (node_type, raw_bytes)
        self.node_offsets: List[int] = []
        self.binary_nodes: List[bytes] = []

    def collect_strings(self, obj: Any):
        """Recursively collect strings from keys and string values."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if not isinstance(k, str):
                    raise TypeError("Only string keys are supported for dicts")
                self._add_string(k)
                self.collect_strings(v)
        elif isinstance(obj, list):
            for e in obj:
                self.collect_strings(e)
        elif isinstance(obj, str):
            self._add_string(obj)
        # bytes, numbers, bool, null: no strings to collect

    def _add_string(self, s: str):
        if s not in self.string_index:
            idx = len(self.strings)
            self.string_index[s] = idx
            self.strings.append(s)



    def build_string_table_node(self) -> bytes:
        """Build a 0xC2 string table node. Returns raw node bytes (including leading type byte)."""
        N = len(self.strings)
        # header: 1 byte type, 3 bytes count
        header = bytes([NODE_STRING_TABLE]) + (0).to_bytes(3, 'little' if self.endian == '<' else 'big')  # placeholder for count; we'll pack with struct
        # We'll pack count using endianness for 3 bytes: easier to build manually
        count_bytes = (N).to_bytes(3, 'little' if self.endian == '<' else 'big')  # count is stored as 3 bytes (endian independent in spec)
        # Offsets array: N+1 offsets (4 bytes each) relative to start of node
        offsets = []
        # The offsets area size = 4*(N+1)
        base_offset = 4 + 4 * (N + 1)  # node header (1+3=4) + offsets
        # Build string data
        string_data = b''
        cur = 0
        for s in self.strings:
            offsets.append(base_offset + cur)
            b = s.encode('utf-8') + b'\x00'
            string_data += b
            cur += len(b)
        offsets.append(base_offset + cur)  # end offset
        # pad offsets area to multiple of 4 already is multiple because it's 4*(N+1)
        # Now assemble
        node = bytearray()
        node.append(NODE_STRING_TABLE)
        node += (N).to_bytes(3, 'little' if self.endian == '<' else 'big')
        for off in offsets:
            node += off.to_bytes(4, 'little' if self.endian == '<' else 'big')  # offsets are relative to start of node; use big-endian for internal offsets
        # append string_data and pad to 4
        node += string_data
        while len(node) % 4 != 0:
            node += b'\x00'
        return bytes(node)

    def encode_value_inline(self, v: Any) -> Tuple[int, bytes]:
        """
        Return (type_byte, 4-byte value) for primitive values that can be encoded inline.
        For strings, returns (VAL_STRING_INDEX, 4-byte index).
        For bytes/binary, returns (NODE_BINARY, offset_placeholder) - caller must replace placeholder with actual offset.
        """
        if v is None:
            return VAL_NULL, (0).to_bytes(4, 'little' if self.endian == '<' else 'big')
        if isinstance(v, bool):
            val = 1 if v else 0
            return VAL_BOOL, val.to_bytes(4, self.endian == '<' and 'little' or 'big', signed=False)
        if isinstance(v, int):
            if v < 0:
                # signed 32-bit
                if not (-2**31 <= v < 2**31):
                    raise ValueError("Integer out of 32-bit range")
                return VAL_INT, int.to_bytes(v & 0xFFFFFFFF, 4, self.endian == '<' and 'little' or 'big', signed=False)
            else:
                if v <= 0x7FFFFFFF:
                    return VAL_INT, int.to_bytes(v, 4, self.endian == '<' and 'little' or 'big', signed=True)
                elif v <= 0xFFFFFFFF:
                    return VAL_UINT, int.to_bytes(v, 4, self.endian == '<' and 'little' or 'big', signed=False)
                else:
                    raise ValueError("Integer out of 32-bit range")
        if isinstance(v, float):
            # pack as float32
            fmt = self.endian + 'f'
            return VAL_FLOAT, struct.pack(fmt, v)
        if isinstance(v, str):
            idx = self.string_index[v]
            # string index is a 4-byte integer (index into string table)
            return VAL_STRING_INDEX, int.to_bytes(idx, 4, self.endian == '<' and 'little' or 'big', signed=False)
        if isinstance(v, bytes):
            # create a binary node and return placeholder offset (0 for now). We'll append node later and replace offsets.
            idx = len(self.binary_nodes)
            self.binary_nodes.append(v)
            # placeholder 0; caller must treat this as a non-regular node and use offset to node
            return NODE_BINARY, (idx).to_bytes(4, 'little' if self.endian == '<' else 'big')
        raise TypeError(f"Unsupported value type: {type(v)}")

    def build_array_node(self, arr: List[Any]) -> bytes:
        """
        Build a 0xC0 array node. We will encode element types (1 byte each, padded to multiple of 4),
        then element values (4 bytes each). For non-regular value nodes (binary), the 4-byte value will be an offset placeholder.
        """
        N = len(arr)
        node = bytearray()
        node.append(NODE_ARRAY)
        node += (N).to_bytes(3, 'little' if self.endian == '<' else 'big')
        # types array (N bytes) padded to multiple of 4
        types = bytearray()
        values = bytearray()
        # For each element, determine type byte and 4-byte value
        for e in arr:
            if isinstance(e, (dict, list)):
                # container: we will create a node for it later; mark type as container (we'll use 0xC0 for arrays and 0x20 for dicts)
                # For now, we will append a placeholder value 0 and store the actual node in self.nodes later.
                if isinstance(e, list):
                    types.append(NODE_ARRAY)
                else:
                    types.append(NODE_HASH)
                values += (0).to_bytes(4, 'little' if self.endian == '<' else 'big')
            else:
                tbyte, vbytes = self.encode_value_inline(e)
                types.append(tbyte)
                values += vbytes
        # pad types to multiple of 4
        while len(types) % 4 != 0:
            types += b'\x00'
        node += types
        # append values (4*N)
        node += values
        # pad node to 4 bytes
        while len(node) % 4 != 0:
            node += b'\x00'
        return bytes(node)

    def build_hash_node(self, d: Dict[str, Any]) -> bytes:
        """
        Build a 0x20 hash node. Entries must be sorted by hash value.
        Each entry: 4-byte hash, 4-byte value (inline or offset placeholder).
        After entries, append N type bytes (1 per entry) padded to 4 bytes.
        """
        items = []
        for k, v in d.items():
            h = hash_key(k)
            items.append((h, k, v))
        items.sort(key=lambda x: x[0])
        N = len(items)
        node = bytearray()
        node.append(NODE_HASH)
        node += (N).to_bytes(3, 'little' if self.endian == '<' else 'big')
        entries = bytearray()
        types = bytearray()
        for h, k, v in items:
            entries += h.to_bytes(4, self.endian == '<' and 'little' or 'big')
            if isinstance(v, (dict, list)):
                # placeholder offset 0
                entries += (0).to_bytes(4, 'little' if self.endian == '<' else 'big')
                if isinstance(v, list):
                    types.append(NODE_ARRAY)
                else:
                    types.append(NODE_HASH)
            else:
                tbyte, vbytes = self.encode_value_inline(v)
                entries += vbytes
                types.append(tbyte)
        # append entries then types padded to 4
        node += entries
        while len(types) % 4 != 0:
            types += b'\x00'
        node += types
        while len(node) % 4 != 0:
            node += b'\x00'
        return bytes(node)

    def stage_nodes(self, root: Any):
        """
        Recursively create node raw bytes for all containers and binary nodes.
        We store nodes in self.nodes in the order they are created. Later we will assign offsets.
        """
        # first collect strings
        self.collect_strings(root)
        # create string table node now (we will place it among nodes)
        string_node = self.build_string_table_node()
        # We'll place string table node first after header (common approach)
        self.nodes.append((NODE_STRING_TABLE, string_node))
        # recursively create container nodes
        def rec(o):
            if isinstance(o, list):
                # create nodes for children first
                for e in o:
                    if isinstance(e, (list, dict)):
                        rec(e)
                node_bytes = self.build_array_node(o)
                self.nodes.append((NODE_ARRAY, node_bytes))
            elif isinstance(o, dict):
                for v in o.values():
                    if isinstance(v, (list, dict)):
                        rec(v)
                node_bytes = self.build_hash_node(o)
                self.nodes.append((NODE_HASH, node_bytes))
            else:
                # primitives and bytes handled elsewhere
                pass
        rec(root)
        # create binary nodes (0xA1) for each bytes entry
        for b in self.binary_nodes:
            node = bytearray()
            # node type is not stored in A1 node body (A1 is a value node type used as offset), but when stored as a full node we just store data block
            # For our representation, we store raw A1 node as: 4-byte length + data
            node += len(b).to_bytes(4, self.endian == '<' and 'little' or 'big')
            node += b
            # pad to 4
            while len(node) % 4 != 0:
                node += b'\x00'
            self.nodes.append((NODE_BINARY, bytes(node)))

    def assign_offsets_and_fix_placeholders(self, header_size=0x10) -> bytes:
        """
        Assign offsets to nodes and produce final bytes. header_size is 0x10 by spec.
        We will place nodes sequentially after header. Return final bytes.
        """
        # compute offsets
        out = bytearray()
        # reserve header
        out += b'\x00' * header_size
        # align to 4 already
        offsets = []
        for node_type, raw in self.nodes:
            # align current length to 4
            cur_off = len(out)
            cur_off = align4(cur_off)
            if cur_off != len(out):
                out += b'\x00' * (cur_off - len(out))
            offsets.append(cur_off)
            out += raw
        # Now we need to go back and fix placeholders in container nodes where we left 0 offsets for child containers and binary nodes.
        # We'll parse each node we created and replace placeholder 4-byte zeros with actual offsets.
        # Build a mapping from node index to offset
        node_offset_map = {i: offsets[i] for i in range(len(self.nodes))}
        # Helper to find node index by identity (we used append order)
        # Node order: [string_table] + container nodes + binary nodes
        # We'll iterate nodes and patch entries.
        out_b = bytearray(out)  # mutable
        for idx, (node_type, raw) in enumerate(self.nodes):
            node_off = offsets[idx]
            if node_type == NODE_ARRAY:
                # parse header: 1 byte type, 3 bytes count
                N = int.from_bytes(raw[1:4], 'little' if self.endian == '<' else 'big')
                types_offset = 4
                # types length padded to multiple of 4
                types_len = align4(N)
                values_offset = 4 + types_len
                for i in range(N):
                    tbyte = raw[types_offset + i]
                    if tbyte in (NODE_ARRAY, NODE_HASH):
                        # placeholder value is at values_offset + 4*i
                        # find the child node in self.nodes by matching raw bytes (approx): we must find the next node of that type that corresponds.
                        # Simpler: we will search for a container in the original structure by scanning nodes after current index for same raw bytes length.
                        # This is heuristic but works for our staged nodes because we created child nodes before parent nodes in staging.
                        # Find first node of matching type that is not the string table and not already referenced.
                        child_idx = None
                        for j in range(len(self.nodes)):
                            if j == idx:
                                continue
                            if self.nodes[j][0] == tbyte:
                                # ensure its offset is not zero and not equal to node_off
                                child_idx = j
                                break
                        if child_idx is None:
                            raise RuntimeError("Could not find child node to patch")
                        child_off = node_offset_map[child_idx]
                        # write offset into out_b at (node_off + values_offset + 4*i)
                        pos = node_off + values_offset + 4 * i
                        out_b[pos:pos+4] = child_off.to_bytes(4, 'little' if self.endian == '<' else 'big')
                # done
            elif node_type == NODE_HASH:
                N = int.from_bytes(raw[1:4], 'little' if self.endian == '<' else 'big')
                entries_offset = 4
                for i in range(N):
                    # hash (4 bytes) then value (4 bytes)
                    value_pos_in_raw = entries_offset + 4 + 8 * i  # raw index where value bytes start
                    # read the type byte from types area: types area starts at entries_offset + 8*N
                    types_area_start = entries_offset + 8 * N
                    tbyte = raw[types_area_start + i]
                    if tbyte in (NODE_ARRAY, NODE_HASH):
                        # find a child node of that type
                        child_idx = None
                        for j in range(len(self.nodes)):
                            if self.nodes[j][0] == tbyte:
                                child_idx = j
                                break
                        if child_idx is None:
                            raise RuntimeError("Could not find child node to patch (hash)")
                        child_off = node_offset_map[child_idx]
                        pos = node_off + value_pos_in_raw
                        out_b[pos:pos+4] = child_off.to_bytes(4, 'little' if self.endian == '<' else 'big')
                    elif tbyte == NODE_BINARY:
                        # value currently contains an index into binary_nodes (we stored that index in encode_value_inline)
                        # raw value bytes are present in raw; we need to read that index and map to the corresponding binary node offset
                        # read the 4 bytes from raw
                        idx_bytes = raw[value_pos_in_raw:value_pos_in_raw+4]
                        idx_val = int.from_bytes(idx_bytes, 'little' if self.endian == '<' else 'big')
                        # binary nodes are appended at the end of self.nodes; find their node index
                        # binary nodes were appended after containers in stage_nodes; find the j-th binary node
                        # find the j-th node with type NODE_BINARY
                        bin_count = -1
                        child_idx = None
                        for j in range(len(self.nodes)):
                            if self.nodes[j][0] == NODE_BINARY:
                                bin_count += 1
                                if bin_count == idx_val:
                                    child_idx = j
                                    break
                        if child_idx is None:
                            raise RuntimeError("Binary node index not found")
                        child_off = node_offset_map[child_idx]
                        pos = node_off + value_pos_in_raw
                        out_b[pos:pos+4] = child_off.to_bytes(4, 'little' if self.endian == '<' else 'big')
                    else:
                        # primitive or string index: nothing to patch
                        pass
            # other node types: nothing to patch
        # Now build header
        # Header layout:
        # 0x00 2 bytes: "BY" (big endian) or "YB" (little endian)
        # 0x02 2 bytes: version (we use 7)
        # 0x04 4 bytes: offset to hash key table (we point to string table node)
        # 0x08 4 bytes: offset to string table (same)
        # 0x0c 4 bytes: offset to root node (we set to last staged node which corresponds to root container)
        header = bytearray(16)
        if self.endian == '>':
            header[0:2] = b'BY'
        else:
            header[0:2] = b'YB'
        header[2:4] = (7).to_bytes(2, 'little' if self.endian == '<' else 'big')  # version 7 stored big-endian in spec; keep consistent
        # hash key table offset and string table offset: point to first node (string table)
        string_table_offset = offsets[0]
        header[4:8] = string_table_offset.to_bytes(4, 'little' if self.endian == '<' else 'big')
        header[8:12] = string_table_offset.to_bytes(4, 'little' if self.endian == '<' else 'big')
        # root node offset: the last node we created that corresponds to the root container.
        # We assume the last container node corresponds to the root (we appended containers after string table)
        # Find the last node that is a container (ARRAY or HASH)
        root_off = 0
        for i in range(len(self.nodes)-1, -1, -1):
            if self.nodes[i][0] in (NODE_ARRAY, NODE_HASH):
                root_off = offsets[i]
                break
        header[12:16] = root_off.to_bytes(4, 'little' if self.endian == '<' else 'big')
        # write header into out_b
        out_b[0:16] = header
        return bytes(out_b)

def yaml_to_byml_v7(yaml_text: str, endian: str = 'little') -> bytes:
    """
    Convert YAML text to BYML v7 bytes.
    endian: 'little' or 'big'
    """
    data = yaml.safe_load(yaml_text)
    eb = '<' if endian == 'little' else '>'
    builder = BYMLBuilder(endian=eb)
    builder.stage_nodes(data)
    final = builder.assign_offsets_and_fix_placeholders(header_size=0x10)
    return final
