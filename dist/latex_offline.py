#! /usr/bin/python3

import argparse
import os
import pathlib
import sys
from typing import List

# Version dependent variables
IM_NAME = "latex_offline"
IM_TAG = "dev"

CONTAINER_NAME = "latex_offline"
LOCAL_USER_ID = os.getuid()

CWD = pathlib.Path(os.getcwd()).resolve()


def fn_nodemon_cmd(mode: str, cmd: str) -> List[str]:
    return [
        "nodemon",
        "--config",
        f"/nodemon_config/{mode}.json",
        "--watch",
        "/data/",
        "--exec",
        f"cd /data && {cmd} > /dev/null",
    ]


def fn_docker_cmd(workdir: pathlib.Path, nodemon_cmd: List[str]) -> List[str]:
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
        f"{IM_NAME}:{IM_TAG}",
    ]
    docker_cmd = base_cmd + nodemon_cmd
    return docker_cmd


def main(argv: List[str]) -> int:

    parser = argparse.ArgumentParser(description="Offline LaTeX compiler")
    parser.add_argument(
        "-w", "--workdir", help="Directory containing source files", default=CWD
    )
    parser.add_argument(
        "-c", "--cmd", help="Command to run to compile LaTeX document", default="make"
    )
    parser.add_argument(
        "-m",
        "--mode",
        help="Watcher mode. auto: compile on file change, manual: compile by typing rs then enter",
        default="auto",
        choices=["auto", "manual"],
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        help="Print the command without executing",
        action="store_true",
    )

    args = parser.parse_args(argv)

    workdir = pathlib.Path(args.workdir).resolve()
    if not workdir.is_dir():
        print(f"{args.workdir} is not a directory", file=sys.stderr)
        return 1

    nodemon_cmd = fn_nodemon_cmd(args.mode, args.cmd)
    docker_cmd = fn_docker_cmd(workdir, nodemon_cmd)
    print(" ".join(docker_cmd))
    if not args.dry_run:
        os.execvp("docker", docker_cmd)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
