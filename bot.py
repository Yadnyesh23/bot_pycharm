import os
from pyrogram import Client, filters
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["telegram_bot"]
users_collection = db["users"]

# Initialize Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Command: Start
@app.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id
    users_collection.update_one({"_id": user_id}, {"$set": {"username": message.from_user.username}}, upsert=True)
    message.reply_text(f"Hello {message.from_user.first_name}! Welcome to my bot.")

# Run the bot
if __name__ == "__main__":
    app.run()
