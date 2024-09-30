# Video Downloader and Transcriber with Whisper

This Python script allows you to download videos from various platforms and automatically transcribe the audio into text using OpenAI's Whisper model. The transcript includes timestamps and is saved in a Markdown file alongside the video information.

## Features

- Download videos from multiple supported platforms using `yt-dlp`.
- Transcribe video audio to text with timestamps using OpenAI's Whisper model.
- Save the transcription, complete with timestamps, in a Markdown file.
- Automatically detects and uses GPU if available.

## Supported Platforms

This script supports downloading videos from a wide variety of platforms via `yt-dlp`, including but not limited to:

- YouTube
- Reddit
- TED Talks
- And many more...

For a full list of supported platforms, refer to the official [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Installation

To run the script, make sure you have the following dependencies installed:

- `yt-dlp` for downloading videos.
- `torch` and `whisper` for transcription using Whisper.
- The Python libraries `json`, `re`, `pathlib`, `subprocess`, and `os` (included in the Python Standard Library).

You can install the necessary Python packages using pip:

```bash
pip install torch whisper
```

Additionally, install `yt-dlp` if you haven’t already:

```bash
pip install yt-dlp
```

## Usage

1. Clone this repository:

```bash
git clone https://github.com/ykon-cell/whisper-video-tool.git
cd whisper-video-tool
```

2. Run the script and provide a video link from any supported platform:

```bash
python download_and_transcribe.py
```

3. When prompted, input the video URL.
4. The script will download the video, transcribe it, and save the transcription with timestamps in a `.md` file inside a folder named after the video.

## Example Output

After running the script, a Markdown file will be created in a folder with the following format:

```
00:00:00,000 --> 00:00:05,000 This is the transcription text for the first segment.
00:00:05,000 --> 00:00:10,000 This is the transcription text for the second segment.
...
Original Video URL: https://www.example.com/example
```


## Future Features

- Support for multiple languages in transcription.
- Improve error handling for different platforms.
