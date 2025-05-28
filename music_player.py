import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from pytgcalls.types.input_stream.quality import HighQualityAudio

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
SESSION = "userbot"
GROUP_ID = int(os.getenv("GROUP_ID"))

app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(app)

@app.on_message(filters.text & filters.chat(GROUP_ID))
async def control(client, message):
    if message.text.startswith("پخش "):
        filename = message.text[5:].strip()
        filepath = os.path.join("music", filename)
        if os.path.exists(filepath):
            await pytgcalls.join_group_call(
                GROUP_ID,
                InputStream(
                    InputAudioStream(filepath, HighQualityAudio())
                )
            )
            await message.reply("🎵 در حال پخش: " + filename)
        else:
            await message.reply("❌ موزیک یافت نشد.")

app.start()
pytgcalls.start()
print("🎶 Music player is ready")
input("Press Enter to exit...\\n")
