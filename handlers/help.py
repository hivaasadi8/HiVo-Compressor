"""ℹ️ راهنما"""
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import SUPPORT_USER
from ui import cards, keyboards


async def cb_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("ℹ️")
    await q.edit_message_text(
        cards.help_card(SUPPORT_USER),
        parse_mode=ParseMode.HTML,
        reply_markup=keyboards.back_menu(),
    )
