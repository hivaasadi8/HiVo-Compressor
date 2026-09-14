"""◀ بازگشت / 🗑 لغو"""
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import USERS_FILE, SUPPORT_USER
from ui import cards, keyboards
from utils import load_json


async def cb_back(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("🏠")
    users = load_json(USERS_FILE, {})
    from core.system import get_best_video_encoder, get_cpu_cores
    await q.edit_message_text(
        cards.welcome(q.from_user.first_name, len(users),
                      get_best_video_encoder(), get_cpu_cores()),
        parse_mode=ParseMode.HTML,
        reply_markup=keyboards.main_menu(SUPPORT_USER),
    )


async def cb_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("🗑 لغو شد")
    await q.edit_message_text(
        cards.error_card("عملیات لغو شد", "هر وقت خواستی فایل جدید بفرست"),
        parse_mode=ParseMode.HTML,
    )
