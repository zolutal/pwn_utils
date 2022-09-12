from argparse import ArgumentParser, Namespace
from os.path import exists, expanduser, realpath
from typing import List
from docker.errors import BuildError, ImageNotFound
from io import BytesIO

import tarfile
import docker
import stat
import sys
import os

def parse_args(args: List[str]) -> Namespace:
    parser: ArgumentParser = ArgumentParser("dwninit")
    parser.add_argument('path', nargs='?', type=str, help="Path to the Dockerfile")
    parser.add_argument('-l', '--libc', type=str, default='', help="Path to libc")
    parser.add_argument('-d', '--ld', type=str, default='', help="Path to ld")

    return parser.parse_args(args)


def dwninit(path: str, libc: str, ld: str):
    # Assume path if not specified
    if path is None:
        path = "./Dockerfile"

    if not exists(expanduser(path)):
        print("Could not find Dockerfile at %s" % path)
        return
    path = realpath(path)
    print("[+] Using Dockerfile at %s" % path)

    ## BUILD DOCKERFILE
    print("[+] Building image...")
    client: docker.DockerClient = docker.from_env()
    dockerfile = open(path, 'rb')
    try:
        client.images.build(fileobj=dockerfile, tag="dwninit:latest", nocache=True)
    except BuildError as e:
        print("Encountered build err '%s' while building Docker file at '%s'" % (str(e), path))
        return

    ## START CONTAINER
    print("[+] Starting Container")
    try:
        image: docker.Image = client.images.get("dwninit")
    except ImageNotFound as e:
        print("Failed to find image '%s'" % "dwninit")
        return

    container = client.containers.run("dwninit", "sleep 30", detach=True)

    ## LOCATE FILES
    if not libc:
        libc = get_libc_path(container)
    if not ld:
        ld = get_ld_path(container)

    ## EXTRACT FILES
    print("[+] Copying libc at path %s" % libc)
    libc_strm, libc_stat = container.get_archive(libc)
    print("[+] Extracting libc to %s" % libc_stat['name'])
    filelike = BytesIO(b"".join(b for b in libc_strm))
    tar = tarfile.open(fileobj=filelike)
    file = tar.extractfile(libc_stat['name'])
    with open(libc_stat['name'], 'wb') as f:
        f.write(file.read())

    print("[+] Copying ld at path %s" % ld)
    ld_strm, ld_stat = container.get_archive(ld)
    print("[+] Extracting ld to %s" % ld_stat['name'])
    filelike = BytesIO(b"".join(b for b in ld_strm))
    tar = tarfile.open(fileobj=filelike)
    file = tar.extractfile(ld_stat['name'])
    with open(ld_stat['name'], 'wb') as f:
        f.write(file.read())
    # Update ld permissions
    mode = os.stat(ld_stat['name']).st_mode
    os.chmod(ld_stat['name'], mode | stat.S_IEXEC)

def get_libc_path(container) -> str:
    ldd_raw: str = container.exec_run("ldd /bin/cat").output.decode()
    ldd_split: List[str] = ldd_raw.split("\n")

    for ldd_line in ldd_split:
        if '/libc' in ldd_line:
            libc_path = ldd_line.strip().split(" ")[-2]
            libc_real = container.exec_run("realpath " + libc_path).output.decode()
            return libc_real.strip()
    raise Exception("Failed to find libc path")

def get_ld_path(container) -> str:
    ldd_raw: str = container.exec_run("ldd /bin/cat").output.decode()
    ldd_split: List[str] = ldd_raw.split("\n")

    for ldd_line in ldd_split:
        if '/ld' in ldd_line:
            ld_path = ldd_line.strip().split(" ")[-2]
            ld_real = container.exec_run("realpath " + ld_path).output.decode()
            return ld_real.strip()
    raise Exception("Failed to find ld path")

def main():
    args: List[str] = sys.argv[1:]
    ns: Namespace = parse_args(args)

    dwninit(ns.path, ns.libc, ns.ld)

if __name__ == "__main__":
    main()
