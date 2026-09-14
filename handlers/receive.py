"""📥 دریافت فایل"""
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import MAX_FILE_SIZE_MB, USERS_FILE, RATE_LIMIT_SECONDS
from core.detector import detect_file_type, get_file_emoji, get_human_category
from ui import cards, keyboards
from utils import load_json


async def cmd_receive(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    obj = None

    if msg.video:      obj = msg.video
    elif msg.document: obj = msg.document
    elif msg.audio:    obj = msg.audio
    elif msg.photo:    obj = msg.photo[-1]
    elif msg.voice:    obj = msg.voice

    if not obj:
        return

    # ─── Rate limit ───
    import time
    now = time.time()
    last = ctx.user_data.get("last_request", 0)
    if now - last < RATE_LIMIT_SECONDS:
        wait = int(RATE_LIMIT_SECONDS - (now - last))
        await msg.reply_text(
            cards.rate_limit_card(wait),
            parse_mode=ParseMode.HTML,
        )
        return
    ctx.user_data["last_request"] = now

    # ─── حجم ───
    size = obj.file_size or 0
    if size > MAX_FILE_SIZE_MB * 1024 * 1024:
        await msg.reply_text(
            cards.error_card(
                f"حجم فایل بیش از {MAX_FILE_SIZE_MB}MB",
                "فایل رو کوچک‌تر کن یا به چند تکه بشکن",
            ),
            parse_mode=ParseMode.HTML,
        )
        return

    # ─── تشخیص نوع ───
    name = getattr(obj, "file_name", f"file_{msg.message_id}")
    mime = getattr(obj, "mime_type", "application/octet-stream")

    # یه تشخیص سریع بر اساس نام و mime
    temp_name = name.lower()
    category = "unknown"
    if mime.startswith("video/") or any(temp_name.endswith(e) for e in [".mp4",".mkv",".avi",".mov",".webm"]):
        category = "video"
    elif mime.startswith("image/"):
        category = "gif" if temp_name.endswith(".gif") else "image"
    elif mime.startswith("audio/"):
        category = "audio"
    elif temp_name.endswith(".pdf") or mime == "application/pdf":
        category = "pdf"
    elif any(temp_name.endswith(e) for e in [".zip",".rar",".7z",".tar",".gz"]):
        category = "archive"

    emoji = get_file_emoji(category)
    human = get_human_category(category)

    # ─── ذخیره در session ───
    ctx.user_data.update({
        "file_id":   obj.file_id,
        "file_name": name,
        "file_size": size,
        "mime":      mime,
        "category":  category,
    })

    # ─── کارت ───
    await msg.reply_text(
        cards.file_received(name, size, human, emoji, mime),
        parse_mode=ParseMode.HTML,
        reply_markup=keyboards.quality_menu(),
    )
