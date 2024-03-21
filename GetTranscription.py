from youtube_transcript_api import YouTubeTranscriptApi
import sys
import os

video_id = sys.argv[1]

url = "https://www.youtube.com/watch?v={video_id}"

transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Create the "transcripts" directory if it doesn't exist
transcripts_dir = 'transcripts'
if not os.path.exists(transcripts_dir):
  os.makedirs(transcripts_dir)

# Create a new transcript file
transcript_file = f'{transcripts_dir}/{video_id}_transcript.txt'
open(transcript_file, 'w').close()

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
  
  print(f"{timeStampString}: {blurb['text']}")
  print(f"(Time Gap: {round(timeGap)}s)\n\n")

  with open(f'transcripts/{video_id}_transcript.txt', 'a') as file:
    file.write(f"{timeStampString}: {blurb['text']}\n")
    file.write(f"(Time Gap: {round(timeGap)}s)\n\n")

# Append timeGaps to the beginning of the file
with open(transcript_file, 'r+') as file:
  content = file.read()
  file.seek(0, 0)
  file.write(f"Large Time Gaps: {timeGaps}\n\n")
  file.write(content)