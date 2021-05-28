from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import csv

with open('times.csv', 'r') as file:
    reader = csv.reader(file, delimiter = '\t')
    next(reader)
    for row in reader:
        row[1] = float(row[1])
        row[2] = float(row[2])
        ffmpeg_extract_subclip("test.mp4", row[1], row[2], targetname=f"{row[0]}.mp4")