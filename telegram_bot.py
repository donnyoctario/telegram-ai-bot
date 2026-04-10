from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq
import os

print("🚀 BOT STARTING...")

# API GROQ
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# MEMORY
user_memory = {}

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = user.username

    if username:
        name = f"@{username}"
    else:
        name = user.first_name if user.first_name else "Teman"

    # reset memory saat start
    user_memory[user.id] = []

    await update.message.reply_text(f"Halo {name}! Saya AI Personal Assistant kamu 🤖")

# HANDLE CHAT
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user = update.message.from_user
    username = user.username
    user_id = user.id

    if username:
        name = f"@{username}"
    else:
        name = user.first_name if user.first_name else "Teman"

    # ambil history user
    history = user_memory.get(user_id, [])

    # tambah input user
    history.append({"role": "user", "content": user_text})

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are a smart assistant helping {name}, a product manager.

Always format your answers:
- Use bullet points
- Use clear paragraphs
- DO NOT use tables
- DO NOT use | symbols
- Keep answers clean and easy to read
- Use *bold* (not **)
- Use - for bullet points
- Avoid special characters that break formatting
"""
                },
                *history
            ]
        )

        reply = response.choices[0].message.content

        # simpan jawaban AI ke memory
        history.append({"role": "assistant", "content": reply})

        # limit memory (biar ga berat)
        user_memory[user_id] = history[-10:]

        MAX_LENGTH = 4000
        for i in range(0, len(reply), MAX_LENGTH):
            await update.message.reply_text(
                reply[i:i+MAX_LENGTH],
                parse_mode="Markdown"
        )

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("⚠️ Terjadi error, coba lagi ya.")

# RUN BOT
app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ BOT RUNNING...")
app.run_polling()