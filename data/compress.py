#!/usr/bin/env python3

import argparse
import lzma
import math
import pathlib
import sys

import dh.utils


def get_args():
    parser = argparse.ArgumentParser(description="(De-)compress files containing shuffle numbers")
    parser.add_argument("-d", "--debug", action="store_true", help="If set, show full stack trace for errors.")
    parser.add_argument("-f", "--force", action="store_true", help="If set, overwrite existing target file.")
    parser.add_argument("path", type=pathlib.Path, help="Path of the input file. If it ends on '.txt', it will be compressed into a '.bin' file. If it ends of '.bin', it will be decompressed into a '.txt' file.")
    args = parser.parse_args()
    return args


def compress(path_in: pathlib.Path, overwrite):
    # in and out filenames
    if not path_in.suffix == ".txt":
        raise RuntimeError("Name of the file to be compressed must end on '.txt'")
    path_out = path_in.with_suffix(".bin")

    # only overwrite if specified
    if (not overwrite) and (path_out.exists()):
        raise FileExistsError(f"Target file '{path_out}' exists already. Use '--force' to overwrite.")
    print(f"Compressing '{path_in}' into '{path_out}'...")

    with open(path_in, "r") as file_in:
        with open(path_out, "wb") as file_out:
            # write magic number - reference to OEIS A002326
            file_out.write(bytes.fromhex("2326"))

            # write version number
            file_out.write(bytes.fromhex("01"))

            # write data (compressed)
            with lzma.open(file_out, "w") as file_out_lzma:
                for (n_line, line) in enumerate(dh.utils.pbar(file_in)):
                    (n_str, s_str) = line.strip().split()
                    (n, s) = (int(n_str), int(s_str))
                    if n != n_line + 1:
                        raise RuntimeError(f"Expected n={n_line + 1}, but got n={n}")
                    file_out_lzma.write(s.to_bytes(
                        length=math.ceil(((n - 1).bit_length() + 1) / 8),
                        byteorder="big",
                        signed=False,
                    ))


def decompress(path_in: pathlib.Path, overwrite):
    # in and out filenames
    if not path_in.suffix == ".bin":
        raise RuntimeError("Name of the file to be decompressed must end on '.bin'")
    path_out = path_in.with_suffix(".txt")

    # only overwrite if specified
    if (not overwrite) and (path_out.exists()):
        raise FileExistsError(f"Target file '{path_out}' exists already. Use '--force' to overwrite.")
    print(f"Decompressing '{path_in}' into '{path_out}'...")

    with open(path_in, "rb") as file_in:
        # read magic number
        magic_number = file_in.read(2)
        if not magic_number == bytes.fromhex("2326"):
            raise RuntimeError("Invalid magic number")

        # read version number
        version_number = int(file_in.read(1).hex())
        if version_number != 1:
            raise NotImplementedError(f"File format version {version_number} is not supported")

        with lzma.open(file_in, "r") as file_in_lzma:
            with open(path_out, "w") as file_out:
                n = 1
                pbar = dh.utils.pbar()
                while True:
                    byte_count = math.ceil(((n - 1).bit_length() + 1) / 8)
                    bytes_ = file_in_lzma.read(byte_count)
                    if len(bytes_) != byte_count:
                        break
                    s = int.from_bytes(
                        bytes=bytes_,
                        byteorder="big",
                        signed=False,
                    )
                    file_out.write(f"{n} {s} \n")
                    pbar.update()
                    n += 1


def main(args):
    if args.path.suffix == ".txt":
        compress(path_in=args.path, overwrite=args.force)
    elif args.path.suffix == ".bin":
        decompress(path_in=args.path, overwrite=args.force)
    else:
        raise RuntimeError("Input file name must end on '.txt' (for compression) or '.bin' (for decompression)")


if __name__ == "__main__":
    args = get_args()
    try:
        main(args=args)
    except Exception as e:
        if args.debug:
            raise e
        else:
            print("ERROR: {} ({})".format(e, type(e).__name__))
            sys.exit(1)
