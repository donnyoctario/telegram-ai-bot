from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# API GROQ
import os
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = user.username

    if username:
        name = f"@{username}"
    else:
        name = user.first_name if user.first_name else "Teman"

    await update.message.reply_text(f"Halo {name}! Saya AI Personal Assistance kamu 🤖")

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
                {"role": "system", "content": f"""
You are a smart assistant helping {name}, a product manager.

Always format your answers:
- Use bullet points
- Use clear paragraphs
- DO NOT use tables
- DO NOT use | symbols
- Make it easy to read in chat (Telegram friendly)
- Use *bold* (not **)
- Use - for bullet points
- Avoid special characters that break formatting
- Keep answers clean and easy to read
"""},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.choices[0].message.content

        MAX_LENGTH = 4000
        for i in range(0, len(reply), MAX_LENGTH):
            await update.message.reply_text(
    reply[i:i+MAX_LENGTH],
    parse_mode="Markdown"
)

    except Exception as e:
        await update.message.reply_text("⚠️ Terjadi error, coba lagi ya.")
        print(e)


app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()