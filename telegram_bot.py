from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq
import os

print("🚀 BOT STARTING...")

# API GROQ
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = user.username

    if username:
        name = f"@{username}"
    else:
        name = user.first_name if user.first_name else "Teman"

    await update.message.reply_text(f"Halo {name}! Saya AI Personal Assistant kamu 🤖")

# HANDLE CHAT
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user = update.message.from_user
    username = user.username

    if username:
        name = f"@{username}"
    else:
        name = user.first_name if user.first_name else "Teman"

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
"""
                },
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.choices[0].message.content

        MAX_LENGTH = 4000
        for i in range(0, len(reply), MAX_LENGTH):
            await update.message.reply_text(
                reply[i:i+MAX_LENGTH]
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