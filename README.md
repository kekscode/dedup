# About

A Python3 Script which can recursively find duplicate files based on sha256
hashes. It uses multiprocessing for hashing.

## Performance

Every provided path is handled in one python process to get I/O parallelization
when scanning multiple volumes. Imagine a server with a local SSD disk, a local
spinning disk and mounted network volumes. The SSD will be scanned quite fast
and the network volumes the slowest. It makes sense to start scanning all these
devices in parallel and combine the results at the very end.

## Usage

Arguments:

    $> ./dupes.py /usr/local/bin /usr/share/dict /usr/sbino

Piped input:

    $> ls -d ../ | ./dupes.py 

Mixing piped input and arguments:

    $> ls -d ../ | ./dupes.py /usr/local/bin /usr/share/dict /usr/sbino

## Debug output

Debug output is supported:

    export LOGLEVEL=DEBUG && gls -d ../ | ./dupes.py /usr/local/bin /usr/share/dict /usr/sbino

## Possible improvements

* Find shortest common path in list of paths to avoid processing e. g.: /tmp
  AND /tmp/dir/
* Add glob filter for ignoring paths
* Skip all files with 0 bytes (maybe not worth optimizing)
