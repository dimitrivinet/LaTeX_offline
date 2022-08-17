#! /usr/bin/python3

import argparse
import os
import pathlib
import sys
from typing import List
import dataclasses
from configparser import ConfigParser

PROG = "latex_offline"

# Version dependent variables
IM_NAME = "dimitrivinet/latex_offline"
IM_VERSION_BASE = "v1.2.0"

CONTAINER_NAME = "latex_offline"
LOCAL_USER_ID = os.getuid()

CWD = pathlib.Path(os.getcwd()).resolve()


@dataclasses.dataclass
class Config:
    workdir: pathlib.Path = CWD
    cmd: str = "make"
    mode: str = "auto"
    dry_run: bool = False
    im_version: str = "light"
    verbose: bool = False
    config_file: pathlib.Path = pathlib.Path(f"{PROG}.ini")

    _allowed_modes = ["auto", "manual"]
    _allowed_versions = ["light", "extra", "full"]
    _var_mappings = {
        "workdir": "Working directory",
        "cmd": "Command",
        "mode": "Mode",
        "dry_run": "Dry run",
        "im_version": "Image version",
        "verbose": "Verbose",
        "config_file": "Config file",
    }

    def __post_init__(self):
        if isinstance(self.workdir, str):
            self.workdir = pathlib.Path(self.workdir).resolve()

        if self.mode not in self._allowed_modes:
            raise ValueError(
                f"Invalid mode: {self.mode}. Excepted one of {self._allowed_modes}."
            )

    def pretty(self) -> str:
        ret: List[str] = []
        ret.append("Config:")
        for k, v in dataclasses.asdict(self).items():
            ret.append(f"  {self._var_mappings[k]}: {v}")

        return "\n".join(ret)

def config_from_file(path: pathlib.Path) -> dict:
    """Load config from file."""

    config = ConfigParser()
    config.read(path)

    if not config.has_section(PROG):
        return {}

    ret = {
        "workdir": config.get(PROG, "workdir", fallback=None),
        "cmd": config.get(PROG, "cmd", fallback=None),
        "mode": config.get(PROG, "mode", fallback=None),
        "dry_run": config.getboolean(PROG, "dry_run", fallback=None),
        "im_version": config.get(PROG, "im_version", fallback=None),
        "verbose": config.getboolean(PROG, "verbose", fallback=None),
        "config_file": config.get(PROG, "config_file", fallback=None),
    }

    # filter Nones
    return {k: v for k, v in ret.items() if v is not None}


def fn_nodemon_cmd(mode: str, cmd: str, verbose: bool) -> List[str]:
    """Create command for nodemon."""

    return [
        "nodemon",
        "--config",
        f"/nodemon_config/{mode}.json",
        "--watch",
        "/data/",
        "--exec",
        f"cd /data && {cmd} > /dev/null" if not verbose else f"cd /data && {cmd}",
    ]


def fn_docker_cmd(
    workdir: pathlib.Path, im_version: str, nodemon_cmd: List[str]
) -> List[str]:
    """Create command for running the docker container."""

    im_tag = f"{IM_VERSION_BASE}-{im_version}"

    base_cmd = [
        "docker",
        "run",
        "-it",
        "--rm",
        "--name",
        f"{CONTAINER_NAME}",
        "-e",
        f"LOCAL_USER_ID={LOCAL_USER_ID}",
        "-v",
        f"{workdir}:/data",
        f"{IM_NAME}:{im_tag}",
    ]
    docker_cmd = base_cmd + nodemon_cmd
    return docker_cmd


def main(argv: List[str]) -> int:

    parser = argparse.ArgumentParser(
        prog=PROG, description="Offline LaTeX compiler with auto reload"
    )
    parser.add_argument(
        "-w", "--workdir", help="Directory containing source files",
    )
    parser.add_argument(
        "-c", "--cmd", help="Command to run to compile LaTeX document",
    )
    parser.add_argument(
        "-m",
        "--mode",
        help="Watcher mode. auto: compile on file change, manual: compile by typing rs then enter",
        choices=["auto", "manual"],
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        help="Print the command without executing",
        action="store_true",
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-v",
        "--im-version",
        help="Set LaTeX Offline image version",
        choices=["light", "extra", "full"],
    )
    parser.add_argument(
        "-f", "--config_file", help="Configuration file",
    )
    parser.add_argument(
        "--verbose",
        help="Show verbose output",
        action="store_true",
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {IM_VERSION_BASE}"
    )

    args = parser.parse_args(argv)
    cli_config = {k: v for k, v in vars(args).items() if v is not None}

    if args.config_file is not None:
        config_file = pathlib.Path(args.config_file).resolve()
        # cli_config.pop("config_file", None)
    elif args.workdir is not None:
        config_file = pathlib.Path(os.path.join(args.workdir, f"{PROG}.ini")).resolve()
    else:
        config_file = CWD / f"{PROG}.ini"
        config_file = config_file.resolve()

    file_config = config_from_file(config_file)

    # if cli_config != {}:
    #     print("using cli config")
    #     args = Config(**cli_config)
    # elif file_config != {}:
    #     print("using file config")
    #     args = Config(**file_config)
    # else:
    #     print("using default config")
    #     args = Config()

    merged = file_config | cli_config
    args = Config(**merged)

    # print(f"{file_config=}")
    # print(f"{cli_config=}")
    # print(f"{merged=}")
    # print()

    workdir = pathlib.Path(args.workdir).resolve()
    if not workdir.is_dir():
        print(f"{args.workdir} is not a directory", file=sys.stderr)
        return 1

    nodemon_cmd = fn_nodemon_cmd(args.mode, args.cmd, args.verbose)
    docker_cmd = fn_docker_cmd(workdir, args.im_version, nodemon_cmd)

    print(args.pretty())
    print()
    print(" ".join(docker_cmd))

    if not args.dry_run:
        os.execvp("docker", docker_cmd)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
