# LaTeX Offline

## Offline LaTeX compiler with auto compilation using Docker and nodemon.

## Installation

### Requirements

- Docker Engine
- Python3
- [optional] GNU-make

### Steps

```bash
make install
```

will install the program in $HOME/.local/bin as latex_offline.

If you want to change the installation directory, specify it with:

```bash
INSTALL_DIR=<install dir> make install
```

To check where `make` will install the file without installing it, run:

```bash
make
# or
INSTALL_DIR=<install dir> make
```

## Usage

```plaintext
usage: latex_offline [-h] [-w WORKDIR] [-c CMD] [-m {auto,manual}] [-d] [-v {light,full}] [-V]

Offline LaTeX compiler with auto reload

optional arguments:
  -h, --help            show this help message and exit
  -w WORKDIR, --workdir WORKDIR
                        Directory containing source files
  -c CMD, --cmd CMD     Command to run to compile LaTeX document
  -m {auto,manual}, --mode {auto,manual}
                        Watcher mode. auto: compile on file change, manual: compile by typing rs then enter
  -d, --dry-run         Print the command without executing
  -v {light,full}, --im-version {light,full}
                        Set LaTeX Offline image version
  -V, --version         show program's version number and exit
```

Example:

```bash
latex_offline --workdir ./work/ --cmd "sh compileall.sh" --mode manual
```

watches for change in the `./work` directory, uses the command `sh compileall.sh` to compile the source files into a PDF, and requires the user to type `rs` then press `Enter` to trigger the compilation.

Configuration with a file is also available. CLI args will overwrite file config.

To get default configuration values for fiel config, run:

```bash
latex_offline --show-default-config
```

Config file with all available configurations and their default values:

```ini
[latex_offline]
workdir=.
cmd=make
mode=auto
dry_run=false
im_version=light
verbose=false
```
