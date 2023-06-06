import sys
import os
import yt_dlp
import requests
import json
from pydub import AudioSegment
from faster_whisper import WhisperModel


def get_video_audio(youtube_url, output_file):
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "outtmpl": output_file
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

# duration is in milliseconds (default is 1 minute)
def split_audio_to_segments(input_file, duration=1*60*1000):
    audio = AudioSegment.from_file(input_file)
    segments = []
    start_time = 0
    while start_time < len(audio):
        end_time = start_time + duration
        segment = audio[start_time:end_time]
        segments.append(segment)
        start_time += duration
    return segments

def transcribe_audio_segment(segment, model, file_format="mp3"):
    with open("temp_segment.mp3", "wb") as f:
        segment.export(f, format=file_format)

    with open("temp_segment.mp3", "rb") as f:
        segments, info = model.transcribe(f, beam_size=5)
        transcript = ''.join([segment.text for segment in segments])
    
    os.remove("temp_segment.mp3")
    return transcript

def main():
    if len(sys.argv) != 2:
        print("Usage: python yt_open_transcript.py [youtube_url]")
        return

    youtube_url = sys.argv[1]
    output_file = "audio_output.mp3"
    get_video_audio(youtube_url, output_file)
    segments = split_audio_to_segments(output_file)
    os.remove(output_file)

    model_size = "large-v2"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    transcript = ""
    for segment in segments:
        segment_transcript = transcribe_audio_segment(segment, model)
        print(segment_transcript+ "\\n")

if __name__ == "__main__":
    main()