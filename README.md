# FileTrack

[CHANGELOG](CHANGELOG.md)

[FileTrack](https://github.com/kyan001/PyFileTrack) is a filetracking cli tool that can track file changes in a certain folder.

## Get Started

```sh
pip install filetrack  # Install

filetrack  # Run FileTrack according filetrack.toml in current folder.
```

## Installation

```sh
# pip
pip install --user filetrack  # install filetrack
pip install --upgrade filetrack # upgrade filetrack
pip uninstall filetrack  # uninstall filetrack

# pipx (recommanded)
pipx install filetrack  # install filetrack through pipx
pipx upgrade filetrack  # upgrade filetrack through pipx
pipx uninstall filetrack  # uninstall filetrack through pipx
```

## Config File

* Config file example: [filetrack.toml]

## Knowledge Base

* Trackings: File hashes to track changes.
* TrackFile: The output file to hold file trackings.
* File Exts: Files that you wanna track with specific extensions. As a list, must have at least 1 value (`["mp3",]`）
* TrackFile Format: Can choose from `TOML` or `JSON`
* Old TrackFile: Autodetect and parse old TrackFile to compared with.
* Usage:
  * Dir: Always using current folder as root folder.
  * New file: Generate a new file list.
  * Double-click on the script: Detect old list file by prefix and suffix.
  * Drag a list file: Using drag & drop file list as the old list file.
