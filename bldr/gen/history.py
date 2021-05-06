from pathlib import Path
from hashlib import sha256
import tarfile

import bldr.util

def targz_pack_atomic(tgz_next_name: Path, tgz_name: Path, source_path: Path):
    """
    Atomically create a new .tar.gz by writing to the "next" .tar.gz
    and renaming when complete
    """
    targz_pack(tgz_next_name, source_path)
    tgz_next_name.rename(tgz_name)

def targz_pack(tgz_name: Path, source_path: Path):
    """
    Create a new .tar.gz from the specified folder

    Examples:
    history/current -> history/current.tar.gz 
    history/generated/current -> history/generated/current.tar.gz 
    """
    with tarfile.open(tgz_name, "w:gz") as tar:
        tar.add(source_path, arcname=source_path.name)

def targz_unpack(tgz_path: Path, target_path: Path):
    """
    Expand a .tar.gz to the specified folder

    Examples:
    history/current.tar.gz -> history/current 
    history/generated/current.tar.gz -> history/generated/current 
    """
    if not tgz_path.exists():
        target_path.mkdir(parents=True, exist_ok=True)
        return

    if target_path.exists():
        bldr.util.rmtree(target_path)

    target_path.mkdir(parents=True)

    with tarfile.open(tgz_path, "r:gz") as tar:
        tar.extractall(path=target_path.parent)

def targz_sha(tgz_path: Path):
    return sha256(tgz_path.read_bytes()).hexdigest()