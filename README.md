# yt-open-transcript

Get the transcript of a youtube video. This uses yt-dlp and faster-whisper locally. No need for an API call to OpenAI's whisper. faster-whisper works with the GPU or also the CPU.

## Setup

install everything

```
pip install -r requirements.txt
```

## Usage

```
python3 yt_open_transcript.py "youtube-url"
```

for example:

```
python3 yt_open_transcript.py "https://www.youtube.com/watch?v=65Sd-L03X84"
```
