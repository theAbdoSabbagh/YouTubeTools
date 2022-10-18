import pytube, os

from pydub import AudioSegment
from discord import Interaction
from pytube import YouTube, StreamQuery, Stream
from jishaku.functools import executor_function
from tqdm import tqdm
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from pydub import AudioSegment
import numpy as np

@executor_function
def download_video(interaction : Interaction, url : str, resolution : str):
  try:
    yt = YouTube(url)
  except pytube.exceptions.RegexMatchError:
    return False

  resolutions = ["720p", "480p", "360p", "240p", "144p"]
  yt_streams : StreamQuery = yt.streams
  videos = yt_streams.filter(file_extension = "mp4", resolution = resolution)
  for res in resolutions:
    if not videos:
      if res == resolution:
        continue
      videos = yt_streams.filter(file_extension = "mp4", resolution = res)
    else:
      break
  
  if not videos:
    return None
  
  filesizes = [item.filesize for item in videos]
  video : Stream = videos[filesizes.index(min(filesizes))]
  video_path = video.download(output_path = f"/home/sxvxge/Desktop/YouTubeTools/downloads/{interaction.user.id}")
  
  return video_path

@executor_function
def download_mp3(interaction : Interaction, url : str):
  try:
    yt = YouTube(url)
  except pytube.exceptions.RegexMatchError:
    return False

  yt_streams : StreamQuery = yt.streams
  videos = yt_streams.filter(only_audio = True)
  
  if not videos:
    return None
  
  filesizes = [item.filesize for item in videos]
  video : Stream = videos[filesizes.index(min(filesizes))]
  old_video_path = video.download(output_path = f"/home/sxvxge/Desktop/YouTubeTools/downloads/{interaction.user.id}")
  
  audio_to_mp3(old_video_path)
  os.remove(old_video_path)
  final_video_path = old_video_path.split('/')[-1].split('.')[-1]

  return final_video_path

def audio_to_mp3(path : str):
  extension = path.split('/')[-1].split('.')[-1]
  pre_conversion = AudioSegment.from_file(path, extension)
  post_conversion = pre_conversion.export(path.replace(extension, "mp3"), format = "mp3")

  return post_conversion

@executor_function
def mp3_to_8d(inputfile, outputfile, period = 200):
  # credit to https://github.com/dakshj48/8D-Audio-Converter/

  period = period if period > 0 else 200

  audio = AudioSegment.from_file(inputfile, format='mp3')
  audio = audio + AudioSegment.silent(duration=150)
  fileinfo = MP3(inputfile, ID3=EasyID3)

  eightD = AudioSegment.empty()
  pan = 0.9*np.sin(np.linspace(0, 2*np.pi, period))
  chunks = list(enumerate(audio[::100]))

  for i, chunk in tqdm(chunks, desc='Converting', unit='chunks', total=len(chunks)):
    if len(chunk) < 100:
      continue
    newChunk = chunk.pan(pan[i % period])
    eightD = eightD + newChunk

  eightD.export(outputfile, format='mp3', bitrate=str(fileinfo.info.bitrate))
  return outputfile