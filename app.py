from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw
import sys
import os
import urllib.request, json 
import time
import wget
import shutil
import threading
import subprocess

home=os.path.expanduser("~")
appdata=f'{home}\\AppData\\Roaming'
exited= False

if getattr(sys, 'frozen', False):
  application_path = os.path.dirname(sys.executable)
elif __file__:
  application_path = os.path.dirname(__file__)

if not os.path.isfile(f'{appdata}\\.minecraft\\settings.json'):
  open(f'{appdata}\\.minecraft\\settings.json',"x").write("{\n\"mcv\":\"0.0\",\n\"version\":\"1_19\"}")
appversion = 1.0

if application_path != f'{appdata}\Microsoft\Windows\Start Menu\Programs\Startup':
  version = json.loads(urllib.request.urlopen("https://raw.githubusercontent.com/Dino-VN/Modpack-Autoupdate/main/app.json").read().decode())
  if os.path.isfile(f'{appdata}\Microsoft\Windows\Start Menu\Programs\Startup\MinecraftModpack.exe'):
    os.remove(f'{appdata}\Microsoft\Windows\Start Menu\Programs\Startup\MinecraftModpack.exe')
  wget.download(f"https://github.com/Dino-VN/Modpack-Autoupdate/releases/download/{float(version['app'])}/MinecraftModpack.exe", f'{home}\\AppData\\Local\\Temp\\MinecraftModpack.exe')
  shutil.copy(f'{home}\\AppData\\Local\\Temp\\MinecraftModpack.exe', f"{appdata}\Microsoft\Windows\Start Menu\Programs\Startup\MinecraftModpack.exe")
  os.remove(f'{home}\\AppData\\Local\\Temp\\MinecraftModpack.exe')
  if os.path.isfile(f'{appdata}\Microsoft\Windows\Start Menu\Programs\Startup\MinecraftModpack (1).exe'):
    os.remove(f'{appdata}\Microsoft\Windows\Start Menu\Programs\Startup\MinecraftModpack (1).exe')
  os.system(f"\"{appdata}\Microsoft\Windows\Start Menu\Programs\Startup\MinecraftModpack.exe\"")
  sys.exit(1)

def create_image(width, height, color1, color2):
  # Generate an image and draw a pattern
  image = Image.new('RGB', (width, height), color1)
  dc = ImageDraw.Draw(image)
  dc.rectangle(
    (width // 2, 0, width, height // 2),
    fill=color2)
  dc.rectangle(
    (0, height // 2, width // 2, height),
    fill=color2)

  return image

appicon = create_image(64, 64, 'black', 'white')

def update(aicon, startup):
  settings = json.loads(open(f'{appdata}\\.minecraft\\settings.json').read())
  version = json.loads(urllib.request.urlopen("https://raw.githubusercontent.com/Dino-VN/Modpack-Autoupdate/main/app.json").read().decode())
  mcversion = settings["mcv"]
  if startup: time.sleep(10)
  if float(appversion) != float(version['app']):
    aicon.notify(f"Đang update app từ {float(appversion)} -> {float(version['app'])}")
    wget.download(f"https://github.com/Dino-VN/Modpack-Autoupdate/releases/download/{float(version['app'])}/MinecraftModpack.exe", f'{home}\\AppData\\Local\\Temp\\MinecraftModpack.exe')
    # os.system(f'{home}\\AppData\\Local\\Temp\\MinecraftModpack.exe')
    subprocess.call(f'{home}\\AppData\\Local\\Temp\\MinecraftModpack.exe')
    os.remove(f'{home}\\AppData\\Local\\Temp\\MinecraftModpack.exe')
  if float(mcversion) != float(version['mod']):
    aicon.notify(f"Đang update Modpack từ {float(mcversion)} -> {float(version['mod'])}")
    aicon.notify(f"Đang thoát minecraft")
    subprocess.call(f'taskkill /IM javaw.exe /F')
    wget.download(version[settings["version"]], f'{home}\\AppData\\Local\\Temp\\modpack.zip')
    shutil.rmtree(f"{appdata}\\.minecraft\\mods", ignore_errors=True)
    shutil.unpack_archive(f'{home}\\AppData\\Local\\Temp\\modpack.zip', f"{appdata}\\.minecraft")
    open(f'{appdata}\\.minecraft\\settings.json',"w").write("{\n\"mcv\":\""+version['mod']+"\",\n\"version\":\""+settings["version"]+"\"}")
    aicon.notify(f"Đẫ update Modpack lên bản {float(version['mod'])}")
    os.remove(f'{home}\\AppData\\Local\\Temp\\modpack.zip')

stop_threads = False

def exit(aicon, item):
  aicon.notify('Đang thoát')
  aicon.stop()
  global stop_threads
  stop_threads = True

# To finally show you icon, call run
systray = icon('Minecraft', appicon, menu=menu(
  item(
    'Kiểm tra cập nhập',
    update,
    checked=lambda  item: None
  ),
  # item(
  #   'Phiên bản',
  #   menu(
  #     item(
  #       'Show message',
  #       lambda icon, item: icon.notify('Hello World!')),
  #     item(
  #       'Submenu item 2',
  #       lambda icon, item: icon.remove_notification())
  #   )
  # ),
  item(
    'Thoát',
    exit,
    checked=lambda  item: None
  )
))
systray.run_detached()

def background():
  while True:
    if stop_threads: break
    update(systray, True)
    time.sleep(30)

a = threading.Thread(name='background', target=background)
a.start()