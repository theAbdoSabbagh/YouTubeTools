from discord.ext import commands
from discord.ext.commands import Bot, Cog

class ErrorHandler(Cog):
  """Error handler for the bot."""

  def __init__(self, bot):
    self.bot : Bot = bot
    self.hidden = True

  @Cog.listener("on_command_error")
  async def error_handler(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
      return # no need to fill up the console with this error as it can be frequent
    else:
      print(error.original)

async def setup(bot : Bot):
  await bot.add_cog(ErrorHandler(bot))