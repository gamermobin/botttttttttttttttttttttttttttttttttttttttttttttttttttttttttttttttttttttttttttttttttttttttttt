import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask

# --- تنظیم API ها ---
TELEGRAM_TOKEN = "8126930463:AAFC_RZZIRrutpqVY_8o9E0qvwaaBC2u-YE"
GEMINI_API_KEY = "AIzaSyBQhSmCbsEhatk0dgyT6Xlkh-cOUxiaESo"

# --- پیکربندی مدل Gemini ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# --- ایجاد اپ Flask برای رندر (در صورت نیاز به وب‌هوک) ---
app = Flask(name)

@app.route("/")
def home():
    return "ربات در حال اجراست ✅"

# --- پاسخ‌دهی به پیام‌ها ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ خطا در پاسخ‌دهی: {e}")

# --- دستور شروع ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 🤖 من یه چت‌بات هوش مصنوعی هستم. هر چی خواستی بپرس 🙂")

# --- تابع اصلی ---
def main():
    telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ ربات تلگرام روشن شد و منتظر پیام است...")
    telegram_app.run_polling()

# --- اجرای برنامه ---
if name == "main":
    import threading
    import os

    # اجرای تلگرام‌بات در تِرِد جدا
    threading.Thread(target=main).start()

    # اجرای Flask برای رندر (پورت باید مشخص باشه)
    port = int(os.environ.get("PORT", 10000))  # ← اینجا پورت 10000 تنظیم شده
    app.run(host="0.0.0.0", port=port)