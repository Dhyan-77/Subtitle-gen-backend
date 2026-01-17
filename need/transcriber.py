import subprocess
import os 

def extract_audio(video_path,output = "audio.wav"):
    command = [
        "ffmpeg",
        "-y",
        "-i",video_path,
        "-ac","1",
        "-ar","16000",
        output
    ]

    subprocess.run(command,check=True)
    return output