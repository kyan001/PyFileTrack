from __future__ import annotations

import os

import fuzzyfinder
import consolecmdtools as cct
import consoleiotools as cit
import tomllib

from . import Filetrack


__version__ = '0.0.1'


TARGET_EXTS = ["mp3", "m4a"]
HASH_MODE = "CRC32"  # "CRC32", "MD5", "NAME", "PATH", "MTIME"
TARGET_DIR = ""
FORMAT = "toml"


def get_target_dir(config_path: str = "filetrack.toml") -> str:
    if TARGET_DIR:  # if already set, return it
        return TARGET_DIR
    current_dir = cct.get_path(__file__).parent
    if os.path.isfile(config_path):
        with open(config_path, "rb") as fl:
            config = tomllib.load(fl)
        if config and config.get("folder"):
            relative_path = os.path.join(current_dir, config["folder"])
            return cct.get_path(relative_path)  # reveal real path
    return current_dir  # default to current dir


def compare(ft: Filetrack):
    old_trackings = ft.parse(ft.latest)
    ft.generate(
        target_dir=TARGET_DIR,
        exts=TARGET_EXTS,
        hash_mode=HASH_MODE
    )
    if old_trackings and ft.trackings:
        entries_deleted, entries_added = ft.diffs(old_trackings, ft.trackings)
        if entries_deleted or entries_added:
            cit.info("Changes since last time: ✍️")
            for filename in entries_deleted:
                cit.echo(filename, pre="-")
                if entries_added:
                    fuzzy = list(fuzzyfinder.fuzzyfinder(filename, entries_added))
                    if len(fuzzy) > 0:
                        cit.echo(fuzzy[0], pre="+")
                        entries_added.remove(fuzzy[0])
            for filename in entries_added:
                cit.echo(filename, pre="+")
            ft.save()
            ft.cleanup()
        else:
            cit.info("No changes")
    else:
        cit.info("Done")
        ft.save()
        ft.cleanup()


def run_filetrack(config_path: str = "filetrack.toml", dir: str = os.getcwd(), hash_mode: str = "CRC32", target_exts: list[str] = TARGET_EXTS):
    """Run filetrack

    Args:
        config_path (str, optional): The path or the file name of the config file. Defaults to "filetrack.toml".
        folder (str): The folder path of the files to be tracked. Default is the current working folder.
        hash_mode (str, optional): The hash mode. Defaults to "CRC32". Options: "CRC32", "MD5", "NAME", "PATH", "MTIME".
        target_exts (list[str], optional): The target extensions. Defaults to TARGET_EXTS.
    """
    cit.rule("▶ [yellow]Run Filetrack")
    if not dir:
        dir = os.getcwd()
    dir = get_target_dir()
    ft = Filetrack.Trackfile(
        trackfile_dir=cct.get_path(__file__).parent,
        prefix="TrackFile-",
        format=FORMAT,
        host=True,
    )
    cit.info(f"Version: {ft.__version__}")
    cit.info(f"Trackfile Dir: 📂 {ft.trackfile_dir}")
    cit.info(f"Target Dir: 📂 {TARGET_DIR}")
    cit.info(f"Hash Mode: 🧮 {HASH_MODE}")
    cit.info(f"Target Extensions: 📜 {TARGET_EXTS}")
    cit.info(f"Hostname: 💻 {ft.hostname}")
    compare(ft)
    cit.pause()
