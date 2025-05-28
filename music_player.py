import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
TG_SESSION = os.environ.get("TG_SESSION")  # session string

app = Client(
    TG_SESSION,
    api_id=API_ID,
    api_hash=API_HASH
)

call = PyTgCalls(app)

DOWNLOADS_PATH = "downloads"
os.makedirs(DOWNLOADS_PATH, exist_ok=True)


def download_audio(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOADS_PATH}/song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        return f"{DOWNLOADS_PATH}/song.mp3"


@app.on_message(filters.command("play") & filters.private)
async def play_handler(client, message):
    if len(message.command) < 2:
        await message.reply("مثال: /play هایده")
        return

    query = " ".join(message.command[1:])
    await message.reply(f"در حال دانلود {query} از YouTube...")

    audio_path = download_audio(query)
    await message.reply("دانلود شد. در حال پیوستن به تماس صوتی...")

    chat_id = message.chat.id
    await call.join_group_call(chat_id, AudioPiped(audio_path))
    await message.reply("در حال پخش 🎶")


@app.on_message(filters.command("stop") & filters.private)
async def stop_handler(client, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("⏹ پخش متوقف شد")


async def main():
    await app.start()
    await call.start()
    print("ربات موسیقی آماده است.")
    await app.idle()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
