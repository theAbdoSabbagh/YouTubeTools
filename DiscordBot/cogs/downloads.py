import time, random, os

from discord import app_commands, Interaction, File
from discord.ext.commands import Bot, Cog
from typing import Literal
from internal.useful import download_video, download_mp3, mp3_to_8d

class Downloads(Cog):
  """YouTube video downloading commands."""

  def __init__(self, bot):
    self.bot : Bot = bot

  # TODO: Check if filesize is over 8mb for non-boosted servers
  # TODO: If server is boosted, get level and do math accordingly
  # TODO: Use a file uploading service I guess
  # TODO: Make an embed that shows status with animated emojis on different parts of the command, such as "downloading", "converting", etc

  @app_commands.command(name = "mp4", description = "Download videos in MP4 format.")
  @app_commands.describe(url = "The URL of the video you'd like to download, from YouTube.", resolution = "The desired resolution of the video.")
  async def mp4_download(self, interaction : Interaction, url : str, resolution : Literal['720p', '480p', '360p', '240p', '144p'] = '720p'):
    start_time = time.time()
    await interaction.response.defer(ephemeral = True, thinking = True)
    path = await download_video(interaction, url, resolution)

    if path is False:
      return await interaction.followup.send(f"Invalid video URL.")
    if path is None:
      return await interaction.followup.send(f"Couldn't find a video with a matching URL.")

    try:
      await interaction.followup.send(f"Finished downloading the video in {round(time.time() - start_time)}s", file = File(path))
    except:
      await interaction.followup.send(f"Finished downloading the video in {round(time.time() - start_time)}s. However the file size was too big.")

    os.remove(path)
    # TODO: Check if filesize is over 8mb for non-boosted servers
    # TODO: If server is boosted, get level and do math accordingly
    # TODO: Use a file uploading service I guess

  @app_commands.command(name = "mp3", description = "Download videos in MP3 format.")
  @app_commands.describe(url = "The URL of the video you'd like to download, from YouTube.")
  async def mp3_download(self, interaction : Interaction, url : str):
    start_time = time.time()
    await interaction.response.defer(ephemeral = False, thinking = True)
    path = await download_mp3(interaction, url)

    if path is False:
      return await interaction.followup.send(f"Invalid video URL.")
    if path is None:
      return await interaction.followup.send(f"Couldn't find a video with a matching URL.")

    try:
      await interaction.followup.send(f"Finished downloading the video in {round(time.time() - start_time)}s", file = File(path, f"{random.randint(0, 6969)}-{interaction.user.name}.mp3"))
    except:
      await interaction.followup.send(f"Finished downloading the video in {round(time.time() - start_time)}s. However the file size was too big.")

    os.remove(path)
    # TODO: Check if filesize is over 8mb for non-boosted servers
    # TODO: If server is boosted, get level and do math accordingly
    # TODO: Use a file uploading service I guess


  @app_commands.command(name = "8d", description = "Download videos in MP3 format and convert them into 8D.")
  @app_commands.describe(url = "The URL of the video you'd like to download, from YouTube.")
  async def youtube_to_8d(self, interaction : Interaction, url : str):
    start_time = time.time()
    await interaction.response.defer(ephemeral = False, thinking = True)
    path = await download_mp3(interaction, url)

    if path is False:
      return await interaction.followup.send(f"Invalid video URL.")
    if path is None:
      return await interaction.followup.send(f"Couldn't find a video with a matching URL.")

    converted_video_path = await mp3_to_8d(path, path)

    try:
      await interaction.followup.send(f"Finished downloading the video in {round(time.time() - start_time)}s", file = File(converted_video_path, f"{random.randint(0, 6969)}-{interaction.user.name}.mp3"))
    except:
      await interaction.followup.send(f"Finished downloading the video in {round(time.time() - start_time)}s. However the file size was too big.")

    os.remove(path)
    if converted_video_path != path:
      os.remove(converted_video_path)


async def setup(bot : Bot):
  await bot.add_cog(Downloads(bot))