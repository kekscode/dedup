# About

A Python3 Script which can recursively find duplicate files based on sha256
hashes. It uses multiprocessing for hashing.

## Possible improvements

* Find shortest common path in list of paths to avoid processing e. g.: /tmp
  AND /tmp/dir/
* Skip all files with 0 bytes (maybe not worth optimizing)
* Multiprocessing for hashing is not really helpful, because modern CPUs hash
  so fast that I/O is the problem, not processing. Does it help to implement
  parallel dirwalks *and* parallel hashing? This may help if the drives to
  be scanned are slow, like multiple mounted network drives.
