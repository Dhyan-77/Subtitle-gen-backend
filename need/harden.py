import subprocess
import os

def encode(video_path, subtitle, output="output_with_subs.mp4"):
    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vf", f"subtitles={subtitle}",
        output
    ]

    subprocess.run(command, check=True)
    return output




def encodeass(video_path, ass_file, output="output_with_ass.mp4"):
    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vf", f"ass={ass_file}",
        output
    ]

    subprocess.run(command, check=True)
    return output





def encode_one_ass(video_path: str, ass_path: str, output_path: str):
    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vf", f"ass={ass_path}",
        output_path
    ]

    subprocess.run(command, check=True)
    return output_path
