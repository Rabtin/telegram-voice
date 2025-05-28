import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputStream, InputAudioStream
from pytgcalls.types.stream import StreamAudioEnded
from yt_dlp import YoutubeDL

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
SESSION = os.getenv("TG_SESSION", "userbot")
GROUP_ID = int(os.getenv("GROUP_ID"))

app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)
call = PyTgCalls(app)

# دانلود و تبدیل YouTube
def download_youtube_audio(query: str) -> str:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "song.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        filename = ydl.prepare_filename(info["entries"][0])
        return filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")

# هندلر پیام
@app.on_message(filters.text & filters.private)
async def play_command(client: Client, message: Message):
    if message.text.startswith("پخش "):
        query = message.text[5:].strip()
        await message.reply(f"🎵 در حال جستجو و پخش: {query}")

        filename = download_youtube_audio(query)

        await call.join_group_call(
            GROUP_ID,
            InputStream(
                InputAudioStream(
                    filename,
                )
            )
        )
        await message.reply("✅ پخش در تماس صوتی آغاز شد.")

# اجرای برنامه
async def main():
    await app.start()
    await call.start()
    print("🎧 آماده پخش موسیقی در voice call هستم.")
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
