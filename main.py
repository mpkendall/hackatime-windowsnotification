from pystray import MenuItem as item, Menu
import pystray
from PIL import Image, ImageDraw
import requests
import threading
import time
import webbrowser

WAKATIME_API_KEY = ''
API_URL = 'https://hackatime.hackclub.com/api/hackatime/v1/users/current/statusbar/today'

def get_today_time():
    headers = {'Authorization': f'Bearer {WAKATIME_API_KEY}'}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        summary = data['data']['grand_total']['text']
        return summary
    else:
        return "Error"

def create_icon_image():
    image = Image.new('RGB', (64, 64), color=(40, 40, 40))
    draw = ImageDraw.Draw(image)
    draw.rectangle([20, 20, 44, 44], fill=(100, 200, 255))
    return image

def open_hackatime():
    webbrowser.open("https://hackatime.hackclub.com/")

def run_tray():
    icon = pystray.Icon("hackatime")

    def on_quit(icon, item):
        icon.stop()

    icon.menu = Menu(
        item('Quit', on_quit),
        item('Open Hackatime', open_hackatime)
    )

    def update_tooltip():
        while True:
            try:
                today_time = get_today_time()
                icon.title = f"hackatime: {today_time}"
            except Exception as e:
                icon.title = "Error fetching time"
            time.sleep(300)

    icon.icon = create_icon_image()
    icon.title = "WakaTime: Loading..."
    threading.Thread(target=update_tooltip, daemon=True).start()
    icon.run()

run_tray()
