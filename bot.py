import pandas as pd
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

data = pd.read_csv("marks.csv")

TOKEN = os.getenv("BOT_TOKEN")

keyboard = [["📄 Check Result"], ["ℹ️ Help"]]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

user_state = {}

def clean(x):
    return x.upper().replace(" ", "")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎓 DLD LAB. REPORT RESULT OUT OF 15\n\nSelect an option:",
        reply_markup=reply_markup
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if text == "ℹ️ Help":
        await update.message.reply_text("Click Check Result → Enter ID like UGR/5889/18")
        return

    if text == "📄 Check Result":
        user_state[user_id] = "waiting"
        await update.message.reply_text("Enter your Student ID:")
        return

    if user_state.get(user_id) == "waiting":
        df = data.copy()
        df["ID"] = df["ID"].astype(str).apply(clean)

        result = df[df["ID"] == clean(text)]

        if not result.empty:
            row = result.iloc[0]
            await update.message.reply_text(
                f"🎓 RESULT CARD\n"
                f"━━━━━━━━━━━━━━\n"
                f"👤 {row['Name']}\n"
                f"🆔 {row['ID']}\n"
                f"📊 {row['Mark']}\n"
                f"━━━━━━━━━━━━━━\n"
                f"🏫 Wakuma D. | SE Section 3 | Class Rep"
            )
        else:
            await update.message.reply_text("❌ ID not found")

        user_state[user_id] = None

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
