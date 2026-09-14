"""🚀 /start"""
import time
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import USERS_FILE, SUPPORT_USER
from core.system import get_best_video_encoder, get_cpu_cores
from ui import cards, keyboards
from utils import load_json, save_json


async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users = load_json(USERS_FILE, {})

    is_new = str(user.id) not in users
    users[str(user.id)] = {
        "name": user.first_name,
        "username": user.username or "",
        "joined": time.time(),
        "files": users.get(str(user.id), {}).get("files", 0),
        "saved": users.get(str(user.id), {}).get("saved", 0),
    }
    save_json(USERS_FILE, users)

    text = cards.welcome(
        name=user.first_name,
        total_users=len(users),
        encoder=get_best_video_encoder(),
        cores=get_cpu_cores(),
    )

    # ─── GIF خوش‌آمد اگه موجود بود ───
    gif_path = __import__("pathlib").Path("assets/welcome.gif")
    if gif_path.exists():
        with open(gif_path, "rb") as f:
            await update.message.reply_animation(
                animation=f,
                caption=text,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboards.main_menu(SUPPORT_USER),
            )
    else:
        await update.message.reply_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboards.main_menu(SUPPORT_USER),
        )
