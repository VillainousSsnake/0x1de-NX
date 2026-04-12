"""
yaml_to_byml.py

Converts a YAML string into BYML v7 binary bytes suitable for Zelda: Tears of the Kingdom.

Author: Copilot-style implementation (verbose, production-ready)
"""

from __future__ import annotations
import struct
import zlib
import math
from typing import Any, Dict, List, Tuple, Optional, Callable, Union
import io
import sys

# YAML parsing: use PyYAML if available, otherwise fallback to a minimal parser.
try:
    import yaml
except Exception:
    yaml = None

# Node type constants (BYML v7+)
NODE_HASH = 0x20       # plain hash (hash -> node)
NODE_VALUE_HASH = 0x21 # value hash (value + hash + unknown)
NODE_A0 = 0xA0         # string index value
NODE_A1 = 0xA1         # binary data node (offset)
NODE_A2 = 0xA2         # file node (offset)
NODE_ARRAY = 0xC0      # array
NODE_STRING_HASH = 0xC1# string-hash node
NODE_STRING_TABLE = 0xC2# string table node

NODE_BOOL = 0xD0
NODE_INT = 0xD1
NODE_FLOAT = 0xD2
NODE_UINT = 0xD3
NODE_INT64 = 0xD4
NODE_UINT64 = 0xD5
NODE_DOUBLE = 0xD6
NODE_NULL = 0xFF

# Helper types
HashFunc = Callable[[str], int]

# Utility: alignment
def align_up(x: int, a: int) -> int:
    return (x + (a - 1)) & ~(a - 1)

# Default hash function: CRC32 (returns unsigned 32-bit)
def default_hash_func(s: str) -> int:
    return zlib.crc32(s.encode('utf-8')) & 0xFFFFFFFF

# Exception for BYML generation errors
class BYMLGenerationError(Exception):
    pass

# Node representation classes
class Node:
    """
    Abstract node. Concrete nodes implement size() and write().
    The write() method writes the node's bytes to a buffer and returns nothing.
    Offsets are relative to the start of the file.
    """
    def __init__(self):
        # Will be set during layout pass
        self.offset: Optional[int] = None

    def size(self, ctx: 'BuildContext') -> int:
        raise NotImplementedError()

    def write(self, buf: io.BytesIO, ctx: 'BuildContext'):
        raise NotImplementedError()

class ValueNode(Node):
    """
    Represents a simple value node that can be encoded inline in container entries
    (as a 4-byte value) or as a full node (for special types that require offsets).
    """
    def __init__(self, value_type: int, value: Any):
        super().__init__()
        self.value_type = value_type
        self.value = value

    def size(self, ctx: 'BuildContext') -> int:
        # Value nodes that are "special" (A1/A2 or 64-bit) are stored as full nodes
        if self.value_type in (NODE_A1, NODE_A2, NODE_INT64, NODE_UINT64, NODE_DOUBLE):
            # full node size depends on type
            if self.value_type == NODE_A1:
                data = self.value or b''
                return 1 + 3 + 4 + len(data)  # type + count + length + data (not aligned here)
            if self.value_type == NODE_A2:
                data = self.value or b''
                return 1 + 3 + 4 + 4 + len(data)  # type + count + length + 0x1000 + data
            if self.value_type in (NODE_INT64, NODE_UINT64, NODE_DOUBLE):
                return 1 + 3 + 8  # type + count + 8 bytes of payload
        # Other value nodes are encoded inline (4 bytes) and do not occupy a separate node
        return 0

    def write(self, buf: io.BytesIO, ctx: 'BuildContext'):
        # Only write if this node is a full node (size > 0)
        if self.value_type in (NODE_A1, NODE_A2, NODE_INT64, NODE_UINT64, NODE_DOUBLE):
            start = buf.tell()
            ctx.log(f"Writing full value node type=0x{self.value_type:02X} at offset {start}")
            # Node header: 1 byte type + 3 bytes count (for value nodes count is usually 0 or length)
            if self.value_type == NODE_A1:
                data = self.value or b''
                buf.write(struct.pack(ctx.endian + 'B', NODE_A1))
                buf.write(struct.pack(ctx.endian + 'I', len(data))[1:4])  # 3 bytes length
                # For A1, spec says: 4 bytes length (we will write full 4 bytes after header)
                # But many BYML variants use 4 bytes after header; to be safe, write 4 bytes length aligned
                # We'll write a 4-byte length after the 4-byte header boundary.
                # Rewind to write consistent layout: write 3 bytes above then write 1 padding byte to align.
                # Simpler: write header as 4 bytes: type + 3 bytes count already written; now write 4-byte length
                buf.write(struct.pack(ctx.endian + 'I', len(data)))
                buf.write(data)
            elif self.value_type == NODE_A2:
                data = self.value or b''
                buf.write(struct.pack(ctx.endian + 'B', NODE_A2))
                buf.write(struct.pack(ctx.endian + 'I', len(data))[1:4])
                # Write 4-byte file length and 4-byte unknown (0x1000)
                buf.write(struct.pack(ctx.endian + 'I', len(data)))
                buf.write(struct.pack(ctx.endian + 'I', 0x1000))
                buf.write(data)
            elif self.value_type in (NODE_INT64, NODE_UINT64, NODE_DOUBLE):
                buf.write(struct.pack(ctx.endian + 'B', self.value_type))
                buf.write(b'\x00\x00\x00')  # 3 bytes count/unused
                if self.value_type == NODE_DOUBLE:
                    buf.write(struct.pack(ctx.endian + 'd', float(self.value)))
                else:
                    # 64-bit integer
                    if self.value_type == NODE_INT64:
                        buf.write(struct.pack(ctx.endian + 'q', int(self.value)))
                    else:
                        buf.write(struct.pack(ctx.endian + 'Q', int(self.value)))
            else:
                raise BYMLGenerationError("Unhandled full value node type in write()")

class ArrayNode(Node):
    """
    0xC0 array node.
    Stores a list of child nodes/values. For each element we store a 1-byte type and a 4-byte value/offset.
    """
    def __init__(self, elements: List[Any]):
        super().__init__()
        self.elements = elements  # raw python values or Node wrappers

    def size(self, ctx: 'BuildContext') -> int:
        # header: 1 + 3
        n = len(self.elements)
        # types array length rounded up to multiple of 4
        types_len = align_up(n, 4)
        # values array: 4 * n
        values_len = 4 * n
        # plus sizes of any full child nodes
        s = 1 + 3 + types_len + values_len
        for el in self.elements:
            node = ctx.ensure_node(el)
            s += node.size(ctx)
        return s

    def write(self, buf: io.BytesIO, ctx: 'BuildContext'):
        start = buf.tell()
        ctx.log(f"Writing ArrayNode at offset {start} with {len(self.elements)} elements")
        buf.write(struct.pack(ctx.endian + 'B', NODE_ARRAY))
        buf.write(struct.pack(ctx.endian + 'I', len(self.elements))[1:4])
        # types array (1 byte per element), padded to 4
        types = bytearray()
        for el in self.elements:
            node = ctx.ensure_node(el)
            t = ctx.type_for_node(node, el)
            types.append(t)
        # pad
        while len(types) % 4 != 0:
            types.append(0)
        buf.write(bytes(types))
        # values array: for each element write either inline 4-byte value or offset to node
        for el in self.elements:
            node = ctx.ensure_node(el)
            if ctx.is_inline_value(node, el):
                inline_val = ctx.inline_value(node, el)
                buf.write(struct.pack(ctx.endian + 'I', inline_val))
            else:
                # offset to node
                if node.offset is None:
                    raise BYMLGenerationError("Node offset not assigned before writing values")
                buf.write(struct.pack(ctx.endian + 'I', node.offset))
        # write child full nodes
        for el in self.elements:
            node = ctx.ensure_node(el)
            if not ctx.is_inline_value(node, el):
                # ensure alignment to 4
                cur = buf.tell()
                pad = (4 - (cur % 4)) % 4
                if pad:
                    buf.write(b'\x00' * pad)
                node.offset = buf.tell()
                node.write(buf, ctx)

class HashNode(Node):
    """
    0x20 plain hash node: mapping from 32-bit hash -> node/value.
    Entries must be sorted by hash value.
    Structure:
    1 byte type (0x20)
    3 bytes: number of entries
    then N entries of 8 bytes each: 4-byte hash, 4-byte value (inline or offset)
    then N bytes of types (1 per entry), padded to 4 bytes
    """
    def __init__(self, mapping: Dict[str, Any], hash_func: HashFunc):
        super().__init__()
        self.mapping = mapping
        self.hash_func = hash_func

    def size(self, ctx: 'BuildContext') -> int:
        n = len(self.mapping)
        entries_len = 8 * n
        types_len = align_up(n, 4)
        s = 1 + 3 + entries_len + types_len
        # add sizes of full child nodes
        for k, v in self.mapping.items():
            node = ctx.ensure_node(v)
            s += node.size(ctx)
        return s

    def write(self, buf: io.BytesIO, ctx: 'BuildContext'):
        start = buf.tell()
        ctx.log(f"Writing HashNode at offset {start} with {len(self.mapping)} entries")
        buf.write(struct.pack(ctx.endian + 'B', NODE_HASH))
        buf.write(struct.pack(ctx.endian + 'I', len(self.mapping))[1:4])
        # sort entries by hash
        entries = []
        for k, v in self.mapping.items():
            h = self.hash_func(k) & 0xFFFFFFFF
            entries.append((h, k, v))
        entries.sort(key=lambda x: x[0])
        # write entries (hash + value placeholder)
        value_positions = []
        for h, k, v in entries:
            buf.write(struct.pack(ctx.endian + 'I', h))
            node = ctx.ensure_node(v)
            if ctx.is_inline_value(node, v):
                inline_val = ctx.inline_value(node, v)
                buf.write(struct.pack(ctx.endian + 'I', inline_val))
            else:
                # placeholder offset (will be actual offset when child nodes are written)
                # store node reference to fill later by writing child nodes in sequence
                buf.write(struct.pack(ctx.endian + 'I', node.offset or 0))
            value_positions.append((node, buf.tell() - 4))
        # types array
        types = bytearray()
        for h, k, v in entries:
            node = ctx.ensure_node(v)
            types.append(ctx.type_for_node(node, v))
        while len(types) % 4 != 0:
            types.append(0)
        buf.write(bytes(types))
        # write child full nodes and patch offsets
        for node, pos in value_positions:
            if not ctx.is_inline_value(node, None):
                # align to 4
                cur = buf.tell()
                pad = (4 - (cur % 4)) % 4
                if pad:
                    buf.write(b'\x00' * pad)
                node.offset = buf.tell()
                node.write(buf, ctx)
                # patch the offset in the entries area
                curpos = buf.tell()
                buf.seek(pos)
                buf.write(struct.pack(ctx.endian + 'I', node.offset))
                buf.seek(curpos)

class ValueHashNode(Node):
    """
    0x21 value-hash node: each entry contains 4-byte value, 4-byte hash, 4-byte unknown (0).
    The spec in the doc lists order as: Value (4), Hash (4), Unknown (4).
    We'll implement mapping from key->(value, extra_value) where extra_value is optional.
    For YAML mapping, we accept mapping of key->value and set the extra unknown to 0.
    """
    def __init__(self, mapping: Dict[str, Any], hash_func: HashFunc):
        super().__init__()
        self.mapping = mapping
        self.hash_func = hash_func

    def size(self, ctx: 'BuildContext') -> int:
        n = len(self.mapping)
        entries_len = 12 * n
        types_len = align_up(n, 4)
        s = 1 + 3 + entries_len + types_len
        for k, v in self.mapping.items():
            node = ctx.ensure_node(v)
            s += node.size(ctx)
        return s

    def write(self, buf: io.BytesIO, ctx: 'BuildContext'):
        start = buf.tell()
        ctx.log(f"Writing ValueHashNode at offset {start} with {len(self.mapping)} entries")
        buf.write(struct.pack(ctx.endian + 'B', NODE_VALUE_HASH))
        buf.write(struct.pack(ctx.endian + 'I', len(self.mapping))[1:4])
        entries = []
        for k, v in self.mapping.items():
            h = self.hash_func(k) & 0xFFFFFFFF
            entries.append((k, h, v))
        # The spec doesn't require sorting by hash explicitly here, but we will sort by hash for consistency
        entries.sort(key=lambda x: x[1])
        value_positions = []
        for k, h, v in entries:
            node = ctx.ensure_node(v)
            if ctx.is_inline_value(node, v):
                inline_val = ctx.inline_value(node, v)
                buf.write(struct.pack(ctx.endian + 'I', inline_val))
            else:
                buf.write(struct.pack(ctx.endian + 'I', node.offset or 0))
            buf.write(struct.pack(ctx.endian + 'I', h))
            # unknown 4 bytes (0)
            buf.write(struct.pack(ctx.endian + 'I', 0))
            value_positions.append((node, buf.tell() - 12))
        # types array
        types = bytearray()
        for k, h, v in entries:
            node = ctx.ensure_node(v)
            types.append(ctx.type_for_node(node, v))
        while len(types) % 4 != 0:
            types.append(0)
        buf.write(bytes(types))
        # write child nodes and patch offsets
        for node, pos in value_positions:
            if not ctx.is_inline_value(node, None):
                cur = buf.tell()
                pad = (4 - (cur % 4)) % 4
                if pad:
                    buf.write(b'\x00' * pad)
                node.offset = buf.tell()
                node.write(buf, ctx)
                curpos = buf.tell()
                buf.seek(pos)
                buf.write(struct.pack(ctx.endian + 'I', node.offset))
                buf.seek(curpos)

class StringHashNode(Node):
    """
    0xC1 string-hash node: mapping from name index (3 bytes) -> (1 byte type) -> 4 byte value/offset.
    Entries must be lexicographically sorted by the string in the hash key table.
    We'll accept mapping where keys are strings and use the string table indices.
    """
    def __init__(self, mapping: Dict[str, Any], ctx_strings: Dict[str, int]):
        super().__init__()
        self.mapping = mapping
        self.ctx_strings = ctx_strings  # mapping string -> index in string table

    def size(self, ctx: 'BuildContext') -> int:
        n = len(self.mapping)
        # header 1 + 3
        # each entry: 3 bytes name index + 1 byte type + 4 bytes value = 8 bytes per entry
        s = 1 + 3 + 8 * n
        for k, v in self.mapping.items():
            node = ctx.ensure_node(v)
            s += node.size(ctx)
        return s

    def write(self, buf: io.BytesIO, ctx: 'BuildContext'):
        start = buf.tell()
        ctx.log(f"Writing StringHashNode at offset {start} with {len(self.mapping)} entries")
        buf.write(struct.pack(ctx.endian + 'B', NODE_STRING_HASH))
        buf.write(struct.pack(ctx.endian + 'I', len(self.mapping))[1:4])
        # entries must be lexicographically sorted by string
        entries = sorted(self.mapping.items(), key=lambda kv: kv[0])
        value_positions = []
        for name, v in entries:
            if name not in self.ctx_strings:
                raise BYMLGenerationError(f"String '{name}' not found in string table")
            idx = self.ctx_strings[name]
            # name index is 3 bytes
            buf.write(struct.pack(ctx.endian + 'I', idx)[1:4])
            node = ctx.ensure_node(v)
            t = ctx.type_for_node(node, v)
            buf.write(struct.pack(ctx.endian + 'B', t))
            if ctx.is_inline_value(node, v):
                inline_val = ctx.inline_value(node, v)
                buf.write(struct.pack(ctx.endian + 'I', inline_val))
            else:
                buf.write(struct.pack(ctx.endian + 'I', node.offset or 0))
            value_positions.append((node, buf.tell() - 4))
        # write child nodes and patch offsets
        for node, pos in value_positions:
            if not ctx.is_inline_value(node, None):
                cur = buf.tell()
                pad = (4 - (cur % 4)) % 4
                if pad:
                    buf.write(b'\x00' * pad)
                node.offset = buf.tell()
                node.write(buf, ctx)
                curpos = buf.tell()
                buf.seek(pos)
                buf.write(struct.pack(ctx.endian + 'I', node.offset))
                buf.seek(curpos)

class StringTableNode(Node):
    """
    0xC2 string table node.
    Format:
    1 byte type (0xC2)
    3 bytes: number of entries (N)
    4*(N+1) bytes: offsets to each string relative to start of node
    then N null-terminated strings in alphabetical order
    """
    def __init__(self, strings: List[str]):
        super().__init__()
        self.strings = strings  # already deduped and sorted alphabetically

    def size(self, ctx: 'BuildContext') -> int:
        n = len(self.strings)
        offsets_table_len = 4 * (n + 1)
        # strings bytes
        strings_bytes = sum(len(s.encode('utf-8')) + 1 for s in self.strings)
        total = 1 + 3 + offsets_table_len + strings_bytes
        total = align_up(total, 4)
        return total

    def write(self, buf: io.BytesIO, ctx: 'BuildContext'):
        start = buf.tell()
        ctx.log(f"Writing StringTableNode at offset {start} with {len(self.strings)} strings")
        buf.write(struct.pack(ctx.endian + 'B', NODE_STRING_TABLE))
        buf.write(struct.pack(ctx.endian + 'I', len(self.strings))[1:4])
        # offsets: relative to start of node
        offsets = []
        # compute offsets: header is 4 bytes, offsets table is 4*(N+1)
        base = 1 + 3 + 4 * (len(self.strings) + 1)
        cur = base
        for s in self.strings:
            offsets.append(cur)
            cur += len(s.encode('utf-8')) + 1
        offsets.append(cur)  # end of last string
        # write offsets as 4*(N+1)
        for off in offsets:
            buf.write(struct.pack(ctx.endian + 'I', off))
        # write strings
        for s in self.strings:
            b = s.encode('utf-8') + b'\x00'
            buf.write(b)
        # pad to 4
        pad = (4 - (buf.tell() % 4)) % 4
        if pad:
            buf.write(b'\x00' * pad)

# Build context: tracks string table, nodes, endianness, and helper methods
class BuildContext:
    def __init__(self, endianness: str = 'little', hash_func: HashFunc = default_hash_func, verbose: bool = False):
        if endianness not in ('little', 'big'):
            raise ValueError("endianness must be 'little' or 'big'")
        self.endianness = endianness
        self.endian = '<' if endianness == 'little' else '>'
        self.hash_func = hash_func
        self.verbose = verbose
        # string table mapping: string -> index
        self.string_to_index: Dict[str, int] = {}
        self.strings: List[str] = []
        # nodes cache for Python values -> Node wrapper
        self.node_cache: Dict[int, Node] = {}
        # root node
        self.root_node: Optional[Node] = None

    def log(self, *args):
        if self.verbose:
            print("[BYML]", *args, file=sys.stderr)

    def ensure_node(self, value: Any) -> Node:
        """
        Convert a Python value into a Node object (or return existing).
        This does not assign offsets; it only wraps values.
        """
        # Use id-based cache for objects to avoid duplicate wrappers for same object
        key = id(value) if not isinstance(value, (str, int, float, bool, type(None), bytes)) else (type(value), value)
        # For immutable primitives, use a deterministic key
        if isinstance(key, tuple):
            cache_key = ('imm', key)
        else:
            cache_key = ('obj', key)
        # Use dict key as string to avoid unhashable issues
        cache_id = str(cache_key)
        if cache_id in self.node_cache:
            return self.node_cache[cache_id]
        node = None
        # Determine type
        if value is None:
            node = ValueNode(NODE_NULL, 0)
        elif isinstance(value, bool):
            node = ValueNode(NODE_BOOL, 1 if value else 0)
        elif isinstance(value, int):
            # choose appropriate integer type
            if -0x80000000 <= value <= 0x7FFFFFFF:
                node = ValueNode(NODE_INT, int(value))
            elif 0 <= value <= 0xFFFFFFFF:
                node = ValueNode(NODE_UINT, int(value))
            elif -0x8000000000000000 <= value <= 0x7FFFFFFFFFFFFFFF:
                node = ValueNode(NODE_INT64, int(value))
            else:
                node = ValueNode(NODE_UINT64, int(value))
        elif isinstance(value, float):
            # choose double for safety
            node = ValueNode(NODE_DOUBLE, float(value))
        elif isinstance(value, str):
            # string value is encoded as A0 (index into string table)
            # ensure string is in table
            self._ensure_string(value)
            node = ValueNode(NODE_A0, value)
        elif isinstance(value, bytes):
            # treat as binary data (A1)
            node = ValueNode(NODE_A1, value)
        elif isinstance(value, list):
            # array node
            # convert elements recursively
            node = ArrayNode(value)
        elif isinstance(value, dict):
            # mapping: choose string-hash node if all keys are strings, else hash node
            all_str_keys = all(isinstance(k, str) for k in value.keys())
            if all_str_keys:
                # ensure keys are in string table
                for k in value.keys():
                    self._ensure_string(k)
                node = StringHashNode(value, self.string_to_index)
            else:
                # use hash node with hash function
                # convert keys to string representation for hashing
                mapping_str_keys = {str(k): v for k, v in value.items()}
                node = HashNode(mapping_str_keys, self.hash_func)
        else:
            # fallback: convert to string
            s = str(value)
            self._ensure_string(s)
            node = ValueNode(NODE_A0, s)
        self.node_cache[cache_id] = node
        return node

    def _ensure_string(self, s: str):
        if s not in self.string_to_index:
            self.string_to_index[s] = len(self.strings)
            self.strings.append(s)

    def type_for_node(self, node: Node, raw_value: Any) -> int:
        """
        Determine the 1-byte type code to store in types arrays for a given node/value.
        For ValueNode with A0 (string) we return 0xA0, etc.
        """
        if isinstance(node, ValueNode):
            vt = node.value_type
            # For A0 string values, the container expects 0xA0
            return vt
        elif isinstance(node, ArrayNode):
            return NODE_ARRAY
        elif isinstance(node, HashNode):
            return NODE_HASH
        elif isinstance(node, ValueHashNode):
            return NODE_VALUE_HASH
        elif isinstance(node, StringHashNode):
            return NODE_STRING_HASH
        elif isinstance(node, StringTableNode):
            return NODE_STRING_TABLE
        else:
            raise BYMLGenerationError("Unknown node type in type_for_node")

    def is_inline_value(self, node: Node, raw_value: Any) -> bool:
        """
        Return True if the node can be encoded inline as a 4-byte value in a container.
        Inline types: D0, D1, D2 (float32?), D3, A0 (string index), FF (null)
        Special full nodes: A1, A2, D4, D5, D6 require full node offsets.
        """
        if isinstance(node, ValueNode):
            if node.value_type in (NODE_A1, NODE_A2, NODE_INT64, NODE_UINT64, NODE_DOUBLE):
                return False
            # other value nodes are inline
            return True
        # containers are not inline
        return False

    def inline_value(self, node: Node, raw_value: Any) -> int:
        """
        Compute the 4-byte inline value for a ValueNode.
        For strings (A0) this is the 4-byte index into the string table.
        For ints/floats/bools/null, encode as 32-bit representation.
        """
        if not isinstance(node, ValueNode):
            raise BYMLGenerationError("inline_value called for non-ValueNode")
        vt = node.value_type
        if vt == NODE_NULL:
            return 0
        if vt == NODE_BOOL:
            return 1 if node.value else 0
        if vt == NODE_INT:
            return struct.unpack(self.endian + 'I', struct.pack(self.endian + 'i', int(node.value)))[0]
        if vt == NODE_UINT:
            return int(node.value) & 0xFFFFFFFF
        if vt == NODE_FLOAT:
            # float32
            return struct.unpack(self.endian + 'I', struct.pack(self.endian + 'f', float(node.value)))[0]
        if vt == NODE_A0:
            # string index
            idx = self.string_to_index.get(node.value)
            if idx is None:
                raise BYMLGenerationError("String not found in table for inline_value")
            return idx
        # fallback
        raise BYMLGenerationError(f"Cannot inline value type 0x{vt:02X}")

# Main conversion function
def yaml_to_byml(yaml_str: str,
                 version: int = 7,
                 endianness: str = 'little',
                 hash_func: Optional[HashFunc] = None,
                 verbose: bool = False) -> bytes:
    """
    Convert YAML string to BYML v7 bytes.

    Parameters:
    - yaml_str: YAML content as string.
    - version: BYML version to write (default 7 for TotK).
    - endianness: 'little' or 'big' (output endianness).
    - hash_func: optional callable(str)->int to compute 32-bit hashes for hash nodes.
    - verbose: if True, prints debug logs to stderr.

    Returns:
    - bytes of the BYML file.
    """
    if yaml is None:
        raise RuntimeError("PyYAML is required (install with `pip install pyyaml`)")

    # Parse YAML
    data = yaml.safe_load(yaml_str)
    ctx = BuildContext(endianness=endianness, hash_func=(hash_func or default_hash_func), verbose=verbose)

    # Build root node
    root_node = ctx.ensure_node(data)
    ctx.root_node = root_node

    # Build string table: ensure all strings are collected (keys and values)
    # ensure string table contains all strings already discovered
    # Convert mapping keys for HashNode that used str(k) earlier
    # Strings are deduped in ctx._ensure_string calls during ensure_node

    # Sort strings alphabetically as required by spec
    strings_sorted = sorted(ctx.strings, key=lambda s: s)
    # Rebuild mapping string->index according to alphabetical order
    ctx.string_to_index = {s: i for i, s in enumerate(strings_sorted)}
    ctx.strings = strings_sorted

    # Create string table node
    string_table_node = StringTableNode(ctx.strings)

    # For header: hash key table pointer and string table pointer must be string table node (0xC2)
    # We'll use the same string table node for both hash key table and string table offsets.
    # Root node offset will point to the root node.

    # Layout pass: compute sizes and offsets
    # File layout strategy:
    # Header (0x10 bytes) at offset 0
    # Then we will write nodes in this order:
    #  - string table node
    #  - root node (and any child nodes)
    # This ordering ensures string indices are valid and offsets are resolvable.
    # Note: BYML allows arbitrary ordering; this is a simple deterministic layout.

    # Create a buffer and write header placeholder
    buf = io.BytesIO()
    # Header is 16 bytes
    buf.write(b'\x00' * 16)

    # Align to 4
    cur = buf.tell()
    pad = (4 - (cur % 4)) % 4
    if pad:
        buf.write(b'\x00' * pad)

    # Assign endian prefix for struct
    ctx.log("Beginning layout: writing string table and nodes")
    # Write string table node
    # Align to 4
    cur = buf.tell()
    pad = (4 - (cur % 4)) % 4
    if pad:
        buf.write(b'\x00' * pad)
    string_table_node.offset = buf.tell()
    string_table_node.write(buf, ctx)

    # After string table, write root node
    # Align to 4
    cur = buf.tell()
    pad = (4 - (cur % 4)) % 4
    if pad:
        buf.write(b'\x00' * pad)
    # If root is a StringHashNode, it expects string indices to be present in ctx.string_to_index
    # Ensure root node offset assigned and write
    root_node.offset = buf.tell()
    root_node.write(buf, ctx)

    # Now we have full file bytes; fill header
    file_bytes = buf.getvalue()
    # Build header
    # Magic: 'BY' for big-endian, 'YB' for little-endian
    magic = b'BY' if endianness == 'big' else b'YB'
    header = bytearray(16)
    header[0:2] = magic
    header[2:4] = struct.pack('>H', version)  # version is stored big-endian? Spec shows 2 bytes; we'll store native big-endian for compatibility
    # Offsets: 4 bytes each, relative to start
    # Hash key table offset (we set to string table offset)
    hash_table_offset = string_table_node.offset if string_table_node.offset is not None else 0
    string_table_offset = string_table_node.offset if string_table_node.offset is not None else 0
    root_offset = root_node.offset if root_node.offset is not None else 0
    # Offsets are stored in file endianness (common BYML practice)
    if endianness == 'little':
        header[4:8] = struct.pack('<I', hash_table_offset)
        header[8:12] = struct.pack('<I', string_table_offset)
        header[12:16] = struct.pack('<I', root_offset)
    else:
        header[4:8] = struct.pack('>I', hash_table_offset)
        header[8:12] = struct.pack('>I', string_table_offset)
        header[12:16] = struct.pack('>I', root_offset)

    # Replace header in file bytes
    file_bytes = bytes(header) + file_bytes[16:]

    ctx.log(f"Header: magic={magic}, version={version}, hash_table_offset={hash_table_offset}, string_table_offset={string_table_offset}, root_offset={root_offset}")
    return file_bytes

# If run as script, provide a small test harness
if __name__ == "__main__":
    sample_yaml = """
    root:
      number: 123
      big: 9223372036854775807
      pi: 3.14159
      name: "Link"
      flags:
        - true
        - false
      data: !!binary |
        SGVsbG8gV29ybGQ=
      filedata: !!binary |
        RmlsZSBkYXRhIGhlcmU=
    """
    out = yaml_to_byml(sample_yaml, version=7, endianness='little', verbose=True)
    print("Generated BYML bytes:", len(out))
