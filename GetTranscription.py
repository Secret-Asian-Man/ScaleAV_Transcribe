import argparse
import os
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from pytube import extract

# Create an argument parser
parser = argparse.ArgumentParser(description='Get YouTube video transcript')

# Add a verbose argument
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
parser.add_argument('-u', '--url', required=True, help='Input YouTube video URL')

# Parse the command line arguments
args = parser.parse_args()

url = args.url
video_id = None

if "youtube.com" in url:
  video_id = extract.video_id(url)
else:
  video_id = url
  url = f"https://www.youtube.com/watch?v={url}"

video = YouTube(url)
rawTitle = title = video.title

# Process title
title = title.replace(" ", "")
title = title.replace(".", "-")

transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Create the "transcripts" directory if it doesn't exist
transcriptsDir = 'transcripts'
if not os.path.exists(transcriptsDir):
  os.makedirs(transcriptsDir)

# Create a new transcript file
transcriptFile = f'{transcriptsDir}/{title}_transcript.txt'
open(transcriptFile, 'w').close()

# Write the transcript to the file
timeGaps = []
prevTime = 0
for blurb in transcript:
  if len(blurb['text']) == 1:
    continue

  timeGap = blurb['start'] - prevTime
  prevTime = timeStamp = blurb['start']

  hours, remainder = divmod(timeStamp, 3600)
  minutes, seconds = divmod(remainder, 60)

  timeStampString = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

  if timeGap > 300: # 5 minutes
    timeGaps.append(f"{timeStampString}: {round(timeGap)}s")
  
  if args.verbose:
    print(f"{timeStampString}: {blurb['text']}")
    print(f"(Time Gap: {round(timeGap)}s)\n\n")

  with open(transcriptFile, 'a') as file:
    file.write(f"{timeStampString}: {blurb['text']}\n")
    file.write(f"(Time Gap: {round(timeGap)}s)\n\n")

# Append timeGaps to the beginning of the file
with open(transcriptFile, 'r+') as file:
  content = file.read()
  file.seek(0, 0)
  file.write(f"{rawTitle}\n\n")
  file.write(f"Large Time Gaps: {timeGaps}\n\n\n\n")
  file.write(content)