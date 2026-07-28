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
