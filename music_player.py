from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped

from yt_dlp import YoutubeDL

# کانفیگ
API_ID = int("YOUR_API_ID")
API_HASH = "YOUR_API_HASH"
SESSION_STRING = "YOUR_SESSION_STRING"  # با Pyrogram session بساز


app = Client(session_name=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(app)

@app.on_message()
async def play_audio(client, message):
    if message.text.startswith("پخش "):
        url = message.text.split("پخش ", 1)[1]

        with YoutubeDL({'format': 'bestaudio'}) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']

        await pytgcalls.join_group_call(
            chat_id=message.chat.id,
            stream=AudioPiped(audio_url)
        )

@pytgcalls.on_stream_end()
async def stream_end_handler(client: PyTgCalls, update: Update):
    await client.leave_group_call(update.chat_id)

if __name__ == "__main__":
    app.start()
    pytgcalls.start()
    print("Bot is running...")
    import asyncio
    asyncio.get_event_loop().run_forever()
