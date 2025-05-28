from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream.raw import RawAudio
import asyncio

API_ID = int("YOUR_API_ID")
API_HASH = "YOUR_API_HASH"
SESSION_STRING = "YOUR_SESSION_STRING"  # با Pyrogram session بساز

app = Client(session_name=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
call = PyTgCalls(app)

@app.on_message(filters.command("join") & filters.group)
async def join_call(client, message):
    await call.join_group_call(
        chat_id=message.chat.id,
        stream=RawAudio(file_path="test.raw")
    )

@app.on_message(filters.command("leave") & filters.group)
async def leave_call(client, message):
    await call.leave_group_call(message.chat.id)

async def main():
    await app.start()
    await call.start()
    print("Bot is running...")
    await asyncio.get_event_loop().create_future()

asyncio.run(main())
