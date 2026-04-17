from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq
import os

print("🚀 BOT STARTING...")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


user_memory = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = user.username

    if username:
        name = f"@{username}"
    else:
        name = user.first_name if user.first_name else "Teman"


    user_memory[user.id] = []

    await update.message.reply_text(f"Halo {name}! Saya AI Personal Assistant kamu 🤖")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user = update.message.from_user
    username = user.username
    user_id = user.id

    if username:
        name = f"@{username}"
    else:
        name = user.first_name if user.first_name else "Teman"

    history = user_memory.get(user_id, [])
    history.append({"role": "user", "content": user_text})

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are a smart assistant helping {name}, a product manager.

Context about user's boss:
- Boss name: Neel (Niranjan Kumar)
- Role: CTO
- Personality:
  - tends to think like a CPO (product mindset)
  - prefers waterfall over agile
  - often changes direction and can be difficult to work with

If user asks about:
- "bos saya"
- "Neel"
- "Niranjan"

You should answer based on this context.

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

        history.append({"role": "assistant", "content": reply})

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

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ BOT RUNNING...")
app.run_polling()