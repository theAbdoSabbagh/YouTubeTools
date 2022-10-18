import jishaku, discord

from discord import Activity, Intents
from typing import Literal
from discord.ext import commands
from rich import print
from jishaku.help_command import MinimalEmbedPaginatorHelp
from internal.data import internal
from typing import Optional
from pathlib import Path
from internal.logger import Logger
from internal.sensetive import token
# from pytube import YouTube

class YouTubeTools(commands.Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(intents = Intents.all(), help_command = MinimalEmbedPaginatorHelp(), *args, **kwargs)
    self.internal = internal
    self.owner_ids = [852606823092977684]
    self.logger = Logger()

  async def on_ready(self):
    await self.wait_until_ready()

    print(f"[bold black]Discord bot: [bold white]{self.user} [bold white]|| [bold black]Bot ID: [bold white]{self.user.id}")
    await self.load_extension('jishaku')

    for file in Path('cogs').glob('**/*.py'):
      *_tree, _ = file.parts
      try:
        # self.logger.log(f"Loading: {'.'.join(_tree)}.{file.stem}")
        await self.load_extension(f"{'.'.join(_tree)}.{file.stem}")
      except Exception as e:
        self.logger.error(str(e))
    
bot = YouTubeTools(command_prefix = "!", status = discord.Status.dnd)

@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    await ctx.send("Syncing...")
    async with ctx.typing():
      if not guilds:
          if spec == "~":
              synced = await ctx.bot.tree.sync(guild=ctx.guild)
          elif spec == "*":
              ctx.bot.tree.copy_global_to(guild=ctx.guild)
              synced = await ctx.bot.tree.sync(guild=ctx.guild)
          elif spec == "^":
              ctx.bot.tree.clear_commands(guild=ctx.guild)
              await ctx.bot.tree.sync(guild=ctx.guild)
              synced = []
          else:
              synced = await ctx.bot.tree.sync()

          await ctx.send(
              f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
          )
          return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

jishaku.Flags.ALWAYS_DM_TRACEBACK = True
jishaku.Flags.NO_UNDERSCORE = True
jishaku.Flags.HIDE = True
jishaku.Flags.RETAIN = True
jishaku.Flags.FORCE_PAGINATOR = True

bot.run(token)

# TODO: Database system to store user statistics for some upcoming cool commands. Either SQL or JSON