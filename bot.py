import os
import sqlite3
import pandas as pd

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TOKEN, ADMIN_ID

DB_FILE = "students.db"


def database_exists():
    return os.path.exists(DB_FILE)


def excel_to_database(file_name):
    df = pd.read_excel(file_name, dtype=str)
    df.fillna("", inplace=True)

    conn = sqlite3.connect(DB_FILE)

    df.to_sql("students", conn, if_exists="replace", index=False)

    conn.close()
def get_connection():
    return sqlite3.connect(DB_FILE)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not database_exists():
        await update.message.reply_text(
            "📂 لم يتم رفع ملف النتائج بعد.\n\n"
            "إذا كنت الأدمن، أرسل ملف Excel (.xlsx)."
        )
        return

    await update.message.reply_text(
        "👋 أهلاً بك.\n\nأرسل رقم الجلوس للحصول على النتيجة."
    )


async def upload_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ ليس لديك صلاحية.")
        return

    document = update.message.document

    if document is None:
        return

    if not document.file_name.lower().endswith(".xlsx"):
        await update.message.reply_text("❌ الملف يجب أن يكون بصيغة xlsx")
        return

    file = await document.get_file()

    await file.download_to_drive("students.xlsx")

    excel_to_database("students.xlsx")

    await update.message.reply_text(
        "✅ تم تحديث قاعدة البيانات بنجاح."
    )
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not database_exists():
        await update.message.reply_text("❌ لم يتم رفع ملف النتائج بعد.")
        return

    seat_number = update.message.text.strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE `رقم الجلوس` = ?",
        (seat_number,),
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        await update.message.reply_text("❌ رقم الجلوس غير موجود.")
        return

    columns = [item[0] for item in cursor.description]

    message = "📋 نتيجة الطالب\n\n"

    for col, value in zip(columns, row):
        message += f"🔹 {col}: {value}\n"

    conn.close()

    await update.message.reply_text(message)
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.Document.ALL
        upload_excel,
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        search,
    )
)

print("Bot Started...")

app.run_polling()
