from telegram import Update, Document
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import pandas as pd

from config import TOKEN, ADMIN_ID, EXCEL_FILE

students = None


def load_data():
    global students
    students = pd.read_excel(EXCEL_FILE, dtype=str)
    students.fillna("", inplace=True)


load_data()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك.\n\nأرسل رقم الجلوس للحصول على النتيجة."
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    if text.startswith("/"):
        return

    result = students[students.iloc[:, 0] == text]

    if result.empty:
        await update.message.reply_text("❌ رقم الجلوس غير موجود.")
        return

    row = result.iloc[0]

    message = "📋 بيانات الطالب\n\n"

    for col in students.columns:
        value = row[col]
        message += f"🔹 {col}: {value}\n"

    await update.message.reply_text(message)
