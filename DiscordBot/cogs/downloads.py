import time, random, shutil, os

from discord import app_commands, Interaction, File, Embed, InteractionMessage
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

  @app_commands.command(name = "mp4", description = "Download videos in MP4 format.")
  @app_commands.describe(url = "The URL of the video you'd like to download, from YouTube.", resolution = "The desired resolution of the video.")
  async def mp4_download(self, interaction : Interaction, url : str, resolution : Literal['720p', '480p', '360p', '240p', '144p'] = '720p'):
    start_time = time.time()

    embed = Embed(
      title = "Downloading video...",
      description = f"<:pending:1031984015680475277> Video is being downloaded...",
      color = 0x000001
    )
    
    await interaction.response.send_message(embed = embed)
    path = await download_video(interaction, url, resolution)

    if path is False:
      embed.title = "Failed to download video"
      embed.description = "<:failed:1031982289212682332> Invalid video URL."
      return await interaction.edit_original_response(embed = embed)
    if path is None:
      embed.title = "Failed to download video"
      embed.description = "<:failed:1031982289212682332> Couldn't find a video with a matching URL."
      return await interaction.edit_original_response(embed = embed)
    
    try:
      embed.title = "Video downloaded"
      embed.description = f"<:checkmark:1031982292601688144> Video downloaded successfully.\n<:time:1031983535743049809> Downloading time: {round(time.time() - start_time)}s"
      await interaction.edit_original_response(embed = embed, attachments = File(path))
    except:
      embed.title = "Fatal error"
      embed.description = f"<:checkmark:1031982292601688144> Video downloaded successfully.\n<:time:1031983535743049809> Downloading time: {round(time.time() - start_time)}s\n<:failed:1031982289212682332> Failed to upload video due to Discord's upload size limit ({round(os.path.getsize(path)/125000)}MB)"
      await interaction.edit_original_response(embed = embed)

    shutil.rmtree(f"/home/sxvxge/Desktop/YouTubeTools/downloads/{interaction.user.id}")

  @app_commands.command(name = "mp3", description = "Download videos in MP3 format.")
  @app_commands.describe(url = "The URL of the video you'd like to download, from YouTube.")
  async def mp3_download(self, interaction : Interaction, url : str):
    start_time = time.time()

    embed = Embed(
      title = "Downloading audio...",
      description = f"<:pending:1031984015680475277> Audio is being downloaded...",
      color = 0x000001
    )

    await interaction.response.send_message(embed = embed)
    path = await download_mp3(interaction, url)

    if path is False:
      embed.title = "Failed to download audio"
      embed.description = "<:failed:1031982289212682332> Invalid video URL."
      return await interaction.edit_original_response(embed = embed)
    if path is None:
      embed.title = "Failed to download audio"
      embed.description = "<:failed:1031982289212682332> Couldn't find a video with a matching URL."
      return await interaction.edit_original_response(embed = embed)

    try:
      embed.title = "Audio downloaded"
      embed.description = f"<:checkmark:1031982292601688144> Audio downloaded successfully.\n<:time:1031983535743049809> Downloading time: {round(time.time() - start_time)}s"
      await interaction.edit_original_response(embed = embed, attachments = File(path))
    except:
      embed.title = "Fatal error"
      embed.description = f"<:checkmark:1031982292601688144> Audio downloaded successfully.\n<:time:1031983535743049809> Downloading time: {round(time.time() - start_time)}s\n<:failed:1031982289212682332> Failed to upload audio due to Discord's upload size limit ({round(os.path.getsize(path)/125000)}MB)"
      await interaction.edit_original_response(embed = embed)

    shutil.rmtree(f"/home/sxvxge/Desktop/YouTubeTools/downloads/{interaction.user.id}")

  @app_commands.command(name = "8d", description = "Download videos in MP3 format and convert them into 8D.")
  @app_commands.describe(url = "The URL of the video you'd like to download, from YouTube.", period = "The period for 8D switching between both sides.")
  async def youtube_to_8d(self, interaction : Interaction, url : str, period : int):
    start_time = time.time()
    
    embed = Embed(
      title = "Downloading audio...",
      description = f"<:pending:1031984015680475277> Audio is being downloaded...\n<:havent_started:1031982290911383682> Convert to 8D",
      color = 0x000001
    )
    await interaction.response.send_message(embed = embed)
    path = await download_mp3(interaction, url)

    if path is False:
      embed.title = "Failed to download audio"
      embed.description = "<:failed:1031982289212682332> Invalid video URL."
      return await interaction.edit_original_response(embed = embed)
    if path is None:
      embed.title = "Failed to download audio"
      embed.description = "<:failed:1031982289212682332> Couldn't find a video with a matching URL."
      return await interaction.edit_original_response(embed = embed)
    
    conversion_time = time.time()
    embed.title = "Converting audio..."
    embed.description = f"<:checkmark:1031982292601688144> Audio downloaded successfully.\n<:time:1031983535743049809> Downloading time: {round(conversion_time - start_time)}s\n<:pending:1031984015680475277> Converting audio to 8D..."
    await interaction.edit_original_response(embed = embed)
    converted_video_path = await mp3_to_8d(path, path, period)

    try:
      embed.title = "Audio downloaded"
      embed.description = f"<:checkmark:1031982292601688144> Audio downloaded successfully.\n<:time:1031983535743049809> Downloading time: {round(conversion_time - start_time)}s\n<:time:1031983535743049809> Conversion time: {round(time.time() - conversion_time)}s\n<:checkmark:1031982292601688144> Audio converted to 8D successfully."
      await interaction.edit_original_response(embed = embed, attachments = File(path))
    except:
      embed.title = "Fatal error"
      embed.description = f"<:checkmark:1031982292601688144> Audio downloaded successfully.\n<:time:1031983535743049809> Downloading time: {round(conversion_time - start_time)}s\n<:time:1031983535743049809> Conversion time: {round(time.time() - conversion_time)}s\n<:failed:1031982289212682332> Failed to upload audio due to Discord's upload size limit ({round(os.path.getsize(path)/125000)}MB)"
      await interaction.edit_original_response(embed = embed)

    shutil.rmtree(f"/home/sxvxge/Desktop/YouTubeTools/downloads/{interaction.user.id}")


async def setup(bot : Bot):
  await bot.add_cog(Downloads(bot))