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
