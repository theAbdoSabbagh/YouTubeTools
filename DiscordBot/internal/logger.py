import time

from rich import print

class Logger():
  def __init__(self) -> None:
    pass

  def error(self, text : str):
    print(f"[bold red][{time.strftime('%H:%M:%S')} || Error] {text}")

  def success(self, text : str):
    print(f"[bold green][{time.strftime('%H:%M:%S')} || Success] {text}")

  def log(self, text : str):
    print(f"[bold green][{time.strftime('%H:%M:%S')} || YouTubeTools] {text}")