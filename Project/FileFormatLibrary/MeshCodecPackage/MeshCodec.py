import struct
import zstandard as zstd


class MeshCodec:

    @staticmethod
    def compress_mesh_codec(stream):
        src = stream.read()

        mem = bytearray()
        # MCPK
        mem.extend(struct.pack('<I', 1263551309))
        # Version 1.1.0.0
        mem.extend(struct.pack('<BBBB', 1, 1, 0, 0))
        # Flags
        mem.extend(struct.pack('<I', _Func.get_mesh_codec_flags(len(src))))
        # ZSTD bfres with no magic
        mem.extend(_Func.compress_zstd(src))

        return bytes(mem)


class _Func:

    @staticmethod
    def get_mesh_codec_flags(decomp_size):
        aligned = (-decomp_size % 0x1000 + 0x1000) % 0x1000
        decomp_size = decomp_size + aligned
        return ((decomp_size >> 0xc) << 5) + 0xc

    @staticmethod
    def compress_zstd(src):
        cctx = zstd.ZstdCompressor(level=20)
        compressed = cctx.compress(src)
        return compressed
