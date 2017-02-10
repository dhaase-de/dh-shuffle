#!/usr/bin/python3

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
    parser.add_argument("-x", "--executable", default="c/main", type=str, help="executable to be used for the computation")
    parser.add_argument("-j", "--jobs", dest="jobs", default=1, type=int, help="number of parallel processes to spawn")
    parser.add_argument(dest="range", nargs="*", type=int, help="range of numbers for which the shuffle number should be computed, can be specified via zero (default range), one (start=1, end given), or two (start and end given) integers")
    kwargs = vars(parser.parse_args())

    # range of numbers for which the shuffle number should be computed
    range_ = kwargs["range"]
    if len(range_) == 0:
        (start, end) = (1, 100000)
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

    ##
    ## run
    ##

    # temporary output filenames
    outFilenamePattern = "/tmp/dh-shuffle-out.txt.{}"
    outFilenames = tuple(outFilenamePattern.format(nProcess + 1) for nProcess in range(processCount))

    # start sub-processes
    processes = []
    for nProcess in range(processCount):
        processes.append(subprocess.Popen(
            (executable, str(start + nProcess), str(end), str(processCount)),
            stdout=open(outFilenames[nProcess], "w"))
        )

    # monitor results until completion
    pbar = dh.utils.pbar(total=end - start + 1)
    lastFinishedCount = 0
    while True:
        finishedCount=0
        done = True
        for (nProcess, process) in enumerate(processes):
            done = done and (process.poll() is not None)
            finishedCount += wcl(outFilenames[nProcess])

        pbar.update(finishedCount - lastFinishedCount)
        lastFinishedCount = finishedCount

        if done:
            break

        time.sleep(1.0)

    ##
    ## finalize
    ##

    #x


if __name__ == "__main__":
    main()
