"""
This is the class for the ZStandard files (.zs)
"""

import zstandard as zstd
import os


class ZSTD:

    @staticmethod
    def decompress(input_file, output_dir, dictionary):

        # Load the dictionary
        with open(dictionary, 'rb') as f:
            dict_data = f.read()
        zstd_dict = zstd.ZstdCompressionDict(dict_data)

        # Create a decompression context using the dictionary
        dctx = zstd.ZstdDecompressor(dict_data=zstd_dict)

        # Getting the decompressed name of the file
        decompressed_filename = str(os.path.basename(input_file))
        decompressed_filename = decompressed_filename.replace(".zs", "")

        # Decompress the file
        with open(input_file, 'rb') as f_in, open(os.path.join(output_dir, decompressed_filename), 'wb') as f_out:
            f_out.write(dctx.decompress(f_in.read()))
        # Closing the file
        f_out.close()

    @staticmethod
    def compress(input_file, output_file, dictionary):

        # Load the dictionary
        with open(dictionary, "rb") as f:
            dict_data = f.read()
        zstd_dict = zstd.ZstdCompressionDict(dict_data)

        # Create a level 16 compression context using the dictionary
        dctx = zstd.ZstdCompressor(level=16, dict_data=zstd_dict)

        # Compressing the file
        with open(input_file, "rb") as f_in, open(output_file, "wb") as f_out:
            f_out.write(dctx.compress(f_in.read()))

        print("Compressed File")

    @staticmethod
    def read(input_file, dictionary):

        # Load the dictionary
        with open(dictionary, 'rb') as f:
            dict_data = f.read()
        zstd_dict = zstd.ZstdCompressionDict(dict_data)

        # Create a decompression context using the dictionary
        dctx = zstd.ZstdDecompressor(dict_data=zstd_dict)

        # Decompress the file
        with open(input_file, 'rb') as f_in:
            output = dctx.decompress(f_in.read())

        # returning the output
        return output
