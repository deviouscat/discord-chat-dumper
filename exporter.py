import discord
from discord.ext import commands
import os
import aiohttp
import asyncio
import sys
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

meow = commands.Bot(command_prefix="!", intents=intents, self_bot=True)

def safe(name):
    return "".join(c for c in name if c.isalnum() or c in ("_", "-", " ")).strip()

async def create_folders(chat_name):
    if not os.path.exists("text"):
        os.mkdir("text")
    base = os.path.join("text", chat_name)
    if not os.path.exists(base):
        os.mkdir(base)
    att = os.path.join(base, "attachments")
    if not os.path.exists(att):
        os.mkdir(att)
    return base, att

async def download(att, folder, current, total):
    path = os.path.join(folder, att.filename)
    async with aiohttp.ClientSession() as s:
        async with s.get(att.url) as r:
            if r.status == 200:
                with open(path, "wb") as f:
                    f.write(await r.read())

    bar = int((current / total) * 40)
    bar_text = "[" + "#" * bar + "-" * (40 - bar) + "]"
    sys.stdout.write(f"\r{bar_text} {current}/{total}  {att.filename}")
    sys.stdout.flush()

async def export_chat(channel):
    if isinstance(channel, discord.DMChannel):
        cname = safe(channel.recipient.name)
    else:
        cname = safe(channel.name)

    base, att_folder = await create_folders(cname)
    chat_file = os.path.join(base, "chat.txt")

    messages = []
    last = None

    while True:
        batch = await channel.history(limit=100, before=last).flatten() if last else await channel.history(limit=100).flatten()
        if not batch:
            break
        messages.extend(batch)
        last = batch[-1]

    total = len(messages)
    if total == 0:
        print("no messages found")
        return

    print(f"found {total} messages\n")

    lines = []
    att_list = []
    i = 0

    for msg in messages[::-1]:
        i += 1
        user = f"{msg.author} ({msg.author.id})"
        t = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
        content = msg.content.replace("\n", " ")
        lines.append(f"[{t}] {user}: {content}")
        att_list.extend(msg.attachments)

        bar = int((i / total) * 40)
        bar_text = "[" + "#" * bar + "-" * (40 - bar) + "]"
        sys.stdout.write(f"\r{bar_text} {i}/{total}")
        sys.stdout.flush()

    with open(chat_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n\nsaving attachments...\n")

    total_att = len(att_list)
    c = 0

    for a in att_list:
        c += 1
        await download(a, att_folder, c, total_att)

    print("\n\ndone ^_^")

async def safe_close():
    try:
        await meow.close()
    except:
        pass

@meow.event
async def on_ready():
    print(f"logged in as {meow.user}\n")
    cid = input("channel id: ").strip()
    channel = meow.get_channel(int(cid))
    if not channel:
        print("invalid channel")
        await safe_close()
        return
    await export_chat(channel)
    await safe_close()

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

try:
    meow.run(TOKEN, bot=False)
except:
    pass
