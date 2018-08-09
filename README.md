![file-hash](https://raw.githubusercontent.com/joshuaavalon/file_hash/master/image/icon.png "file-hash")

# file-hash

file-hash is a simple command line hashing utility written in Python.

## Requirements

* Python 3.7+ 
* Jinja2 2.10+

You should able to use this with Python < 3.7 if you have [dataclass back port](https://github.com/ericvsmith/dataclasses).

## Usage

### Create a hash

```bash
file_hash hash file.txt
```

### Validate a hash

```bash
file_hash validate file.txt
```

## Options

```bash
usage: file_hash [-h] [-a <algorithm>] [-d] [-r] [-s] [-p <path>]
              [-P [<prefix> [<prefix> ...]]] [-S [<suffix> [<suffix> ...]]]
              [-R <regex>] [-K <size>] [-J <size>]
              <command> <path>

Simple hashing script for files.

positional arguments:
  <command>             hash or validate
  <path>                Starting path

optional arguments:
  -h, --help            show this help message and exit
  -a <algorithm>, --algorithm <algorithm>
                        Algorithm to calculate hash. (Default: md5)
  -d, --dry-run         Enable dry run to check what file will be generated.
  -r, --recursive       Go through directories recursively. Use carefully with -s
  -s, --symlink         Follow symlink. Use carefully with -r
  -p <path>, --report <path>
                        Generate a HTML report.
  -P [<prefix> [<prefix> ...]], --ignore-prefix [<prefix> [<prefix> ...]]
                        Ignore files and directories that start with those prefix. (Default: ["."])
  -S [<suffix> [<suffix> ...]], --ignore-suffix [<suffix> [<suffix> ...]]
                        Ignore files and directories that end with those suffix. (Default: all hashing algorithm)
  -R <regex>, --regex <regex>
                        Only hash the files that match the regular expression. (Default: None)
  -K <size>, --min-size <size>
                        Minimum file size to be hashed. Default unit is Byte.
                        Support KB, GB, TB, PB. e.g. 1KB (Default: None)
  -J <size>, --max-size <size>
                        Maximum file size to be hashed. Default unit is Byte.
                        Support KB, GB, TB, PB. e.g. 1KB (Default: None)
```

Note than `algorithm` and `dry-run` does not work on `validate`.