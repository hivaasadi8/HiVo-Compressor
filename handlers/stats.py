"""📊 آمار"""
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import STATS_FILE, USERS_FILE
from ui import cards, keyboards
from utils import load_json


async def cb_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("📊")

    stats = load_json(STATS_FILE, {})
    users = load_json(USERS_FILE, {})
    stats["users"] = len(users)
    stats["today"] = len(users)  # تخمین ساده

    await q.edit_message_text(
        cards.stats_card(stats),
        parse_mode=ParseMode.HTML,
        reply_markup=keyboards.stats_menu(),
    )
