#!/usr/bin/env python

import os
import subprocess as sp
from argparse import ArgumentParser
from time import time

from pytube import YouTube

_parser = ArgumentParser()
_parser.add_argument("url", type=str, help="URL of the video.")
_parser.add_argument(
    "--format",
    "-f",
    type=str,
    help="Out format.",
    choices=("mp3", "mp4"),
    default="mp3",
)
_parser.add_argument(
    "--out_file",
    "-o",
    type=str,
    help="Custom out file name.",
    required=False,
)
_args = _parser.parse_args()


def get_fname(author: str, title: str, ext) -> str:
    if author and title:
        return f"{author} - {title}.{ext}"
    if title:
        return title
    if author:
        return f"{author} - {int(time()) % 1000}.{ext}"
    return f"{int(time()) % 1000}.{ext}"


def convert_to_mp3(fpath: str, out_fname: str):
    cmd = f'ffmpeg -i "{fpath}" -vn -ab 128k -ar 44100 -y "{out_fname}"'
    sp.call(cmd, shell=True)
    os.remove(fpath)


def download_mp3(yt: YouTube) -> None:
    if _args.out_file is not None:
        fname = _args.out_file
    else:
        fname = get_fname(yt.author, yt.title, "mp3")
    audio_streams = yt.streams.filter(only_audio=True)
    audio = None
    for stream in audio_streams:
        print(stream.audio_codec, stream.codecs, stream.abr, stream.bitrate)
        if audio is None:
            audio = stream
        elif stream.bitrate > audio.bitrate:
            audio = stream
    print(audio)
    try:
        out = audio.download()
        convert_to_mp3(out, fname)
        print("FILE SAVED")
    except:
        print("ERROR")
        raise


def check_if_ffmpeg_exists():
    cmd = f"which ffmpeg"
    if sp.call(cmd, shell=True, stdout=sp.DEVNULL) != 0:
        raise FileNotFoundError("ffmpeg is not installed")


def main():
    check_if_ffmpeg_exists()
    return
    url = _args.url
    yt = YouTube(url)
    if _args.format == "mp3":
        download_mp3(yt)
    elif _args.format == "mp4":
        print("NOT SUPPORTED YET")
    else:
        print("WTF?")


if __name__ == "__main__":
    main()
