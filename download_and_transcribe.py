import os
from pathlib import Path
import subprocess
import json
import torch
import whisper
import re
import shutil 

# Check if yt-dlp is installed
if shutil.which("yt-dlp") is None:
    print("yt-dlp is not installed. Please install it first.")
    exit(1)
    
# Check if CUDA is available
if torch.cuda.is_available():
    print("CUDA is available. Using GPU.")
    device = torch.device("cuda")
else:
    print("CUDA is not available. Using CPU.")
    device = torch.device("cpu")

# Load the Whisper model
model = whisper.load_model("base", device=device)

# Function to transcribe video using Whisper, including timestamps
def transcribe_video_with_timestamps(video_path):
    print("Transcribing video using Whisper (with timestamps)...")
    result = model.transcribe(video_path, task="transcribe" , verbose=True)
    segments = result['segments']
    srt_content = []
    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        start_time_str = f"{int(start_time//3600):02}:{int((start_time%3600)//60):02}:{int(start_time%60):02},{int((start_time%1)*1000):03}"
        end_time_str = f"{int(end_time//3600):02}:{int((end_time%3600)//60):02}:{int(end_time%60):02},{int((end_time%1)*1000):03}"
        srt_content.append(f"{start_time_str} --> {end_time_str}\n{text}\n")
    srt_content = '\n'.join(srt_content)
    print("Video transcription completed (with timestamps).")
    return srt_content

# Function to use yt-dlp to get video information and download video
def get_video_info_and_download(video_url):
    print("Fetching video information using yt-dlp...")
    cmd_info = ['yt-dlp', '-j', video_url]
    result_info = subprocess.run(cmd_info, capture_output=True, text=True)
    if result_info.returncode == 0:
        video_info = json.loads(result_info.stdout)
        author_lin = video_info.get('uploader', 'Unknown')
        author = re.sub(r'[\\/:*?"<>/| ]', '_', author_lin)
        title_lin = video_info.get('title', 'Unknown').replace(' ', '_')
        title = re.sub(r'[\\/:*?"<>/| ]', '_', title_lin)
        safe_title = "".join(x for x in title if x.isalnum() or x in " -_").strip()
        folder_name = f"{author}-{safe_title}"
        print(f"\nVideo Author: {author}\nVideo Title: {title}\nProcessed Title: {safe_title}")

        # Create directory
        try:
            print(f"Creating folder: {folder_name}")
            Path(folder_name).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Error creating folder {folder_name}: {e}")
            return None, None

        # Predefined download path
        download_path_template = os.path.join(folder_name, f"{author}-{safe_title}.%(ext)s")

        # Use yt-dlp to download video
        cmd_download = ['yt-dlp', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4', '-o', download_path_template, video_url]
        try:
            subprocess.run(cmd_download, check=True)
            # After yt-dlp download, locate the actual downloaded file
            downloaded_files = list(Path(folder_name).glob(f"{author}-{safe_title}.mp4"))
            if downloaded_files:
                download_path = str(downloaded_files[0])  # Actual path of the downloaded file
                print(f"\nVideo downloaded to: {download_path}")
                return download_path, folder_name
            else:
                print("Downloaded video file not found.")
                return None, None
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while downloading video: {e}")
            return None, None
    else:
        print("Failed to fetch video information: ", result_info.stderr)
        return None, None

# Define a function to handle the download and transcription process
def download_and_transcribe(video_url):
    download_path, folder_name = get_video_info_and_download(video_url)
    if download_path is None:
        return
    
    # Use Whisper to transcribe video with timestamps
    transcript_with_timestamps = transcribe_video_with_timestamps(download_path)

    # Save the transcription with timestamps to a .md file
    md_path = os.path.join(folder_name, f"{folder_name}.md")
    try:
        with open(md_path, "w", encoding="utf-8") as md_file:
            md_file.write(transcript_with_timestamps)
            # Record the video URL at the end of the file
            md_file.write(f"\n\nOriginal Video URL: {video_url}")
        print(f"Transcription with timestamps saved to Markdown file: {md_path}")
    except Exception as e:
        print(f"Error writing to file {md_path}: {e}")

# Input video link
video_url = input("Enter the video link: ")
download_and_transcribe(video_url)
