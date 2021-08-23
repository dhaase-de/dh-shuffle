#!/usr/bin/env python3

import argparse
import os.path
import subprocess
import time

import dh.utils


###
#%% helpers
###


def wcl(filename):
    """
    Count lines of file `filename`.

    .. seealso:: http://stackoverflow.com/a/27517681/1913780
    """

    def _make_gen(reader):
        b = reader(1024 * 1024)
        while b:
            yield b
            b = reader(1024 * 1024)

    f = open(filename, "rb")
    f_gen = _make_gen(f.raw.read)
    return sum(buf.count(b"\n") for buf in f_gen)


###
#%% main
###


def main():
    ##
    ## command line arguments
    ##

    # parse
    parser = argparse.ArgumentParser(description="Wrapper for shuffle number computation.")
    parser.add_argument("-x", "--executable", dest="executable", type=str, default="c/main", help="executable to be used for the computation")
    parser.add_argument("-j", "--jobs", dest="jobs", type=int, default=1, help="number of parallel processes to spawn")
    parser.add_argument("-o", "--outfile", dest="outfile", type=str, required=True, help="output filename")
    parser.add_argument(dest="range", nargs="*", type=int, help="range of numbers for which the shuffle number should be computed, can be specified via zero (default range), one (start=1, end given), or two (start and end given) integers")
    kwargs = vars(parser.parse_args())

    # range of numbers for which the shuffle number should be computed
    range_ = kwargs["range"]
    if len(range_) == 0:
        (start, end) = (1, 10000)
    elif len(range_) == 1:
        (start, end) = (1, int(range_[0]))
    elif len(range_) == 2:
        (start, end) = (int(range_[0]), int(range_[1]))
    else:
        raise ValueError("Range must be specified via zero (default range), one (start=1, end given), or two (start and end given) integers")

    # number of parallel jobs
    processCount = kwargs["jobs"]

    # check executable which will be used for the computation
    executable = kwargs["executable"]
    if not os.path.exists(executable):
        raise FileNotFoundError("Executable not found: '{}'".format(executable))

    # output filename
    outFilename = kwargs["outfile"]

    ##
    ## run
    ##

    # temporary output filenames
    tmpFilenamePattern = "/tmp/dh-shuffle-out.txt.{}"
    tmpFilenames = tuple(tmpFilenamePattern.format(nProcess + 1) for nProcess in range(processCount))

    # start sub-processes
    processes = []
    for nProcess in range(processCount):
        processes.append(subprocess.Popen(
            (executable, str(start + nProcess), str(end), str(processCount)),
            stdout=open(tmpFilenames[nProcess], "w"))
        )

    # monitor results until completion
    pbar = dh.utils.pbar(total=end - start + 1)
    lastFinishedCount = 0
    while True:
        finishedCount=0
        done = True
        for (nProcess, process) in enumerate(processes):
            done = done and (process.poll() is not None)
            finishedCount += wcl(tmpFilenames[nProcess])

        pbar.update(finishedCount - lastFinishedCount)
        lastFinishedCount = finishedCount
        if done:
            break
        time.sleep(1.0)

    ##
    ## finalize
    ##

    print("Merging results into file '{}'...".format(outFilename))
    fs = tuple(open(tmpFilename, "r") for tmpFilename in tmpFilenames)
    with open(outFilename, "w") as o:
        while True:
            lines = tuple(f.readline() for f in fs)
            lines = tuple(line for line in lines if len(line) > 0)
            if len(lines) > 0:
                for line in lines:
                    o.write(line)
            else:
                break


if __name__ == "__main__":
    main()
