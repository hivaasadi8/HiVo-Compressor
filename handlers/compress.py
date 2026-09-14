"""⚙️ فشرده‌سازی کامل با گرافیک زنده"""
import time
from pathlib import Path

from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ContextTypes

from config import TEMP_DIR, STATS_FILE, USERS_FILE
from core.compressor import UniversalCompressor
from core.system import get_best_video_encoder
from ui import cards, keyboards
from ui.progress import LiveProgress
from utils import load_json, save_json


async def cb_quality(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("🚀 شروع شد!")

    # ─── استخراج mode از callback data: "q:fast" ───
    mode = q.data.split(":", 1)[1] if ":" in q.data else "balanced"

    file_id   = ctx.user_data.get("file_id")
    file_name = ctx.user_data.get("file_name", "file")
    size      = ctx.user_data.get("file_size", 0)
    mime      = ctx.user_data.get("mime", "")

    if not file_id:
        await q.edit_message_text(
            cards.error_card("فایل پیدا نشد", "دوباره فایل رو بفرست"),
            parse_mode=ParseMode.HTML,
        )
        return

    # ─── مرحله ۱: آماده‌سازی ───
    await q.edit_message_text(
        cards.preparing(file_name, mode),
        parse_mode=ParseMode.HTML,
    )

    input_path = TEMP_DIR / file_name
    output_path = None

    try:
        # ─── مرحله ۲: دانلود ───
        await q.edit_message_text(
            cards.downloading(file_name, size, 0),
            parse_mode=ParseMode.HTML,
        )
        tg_file = await ctx.bot.get_file(file_id)
        await tg_file.download_to_drive(input_path)

        # ─── مرحله ۳: فشرده‌سازی با progress ───
        start_t = time.time()

        async def edit_func(text):
            try:
                await q.edit_message_text(text, parse_mode=ParseMode.HTML)
            except Exception:
                pass

        def card_func(pct, elapsed, eta):
            return cards.compressing(
                file_name, pct, elapsed, eta,
                stage="Encoding",
                encoder=get_best_video_encoder(),
                mode_label={"fast":"⚡ سریع","balanced":"⚖️ متعادل","max":"💎 کیفیت"}.get(mode, mode),
            )

        live = LiveProgress(edit_func, card_func, min_interval=2.5)

        # آپدیت اولیه
        await edit_func(card_func(0, 0, 0))

        await ctx.bot.send_chat_action(q.message.chat_id, ChatAction.UPLOAD_DOCUMENT)

        result, output_path = await UniversalCompressor.compress(
            input_path, mode, live.update,
        )

        elapsed = time.time() - start_t

        # ─── مرحله ۴: نتیجه ───
        await edit_func(cards.result(
            result["original_size"],
            result["compressed_size"],
            result["ratio"],
            result.get("encoder", "auto"),
            elapsed,
            mode,
        ))
        await q.edit_message_reply_markup(reply_markup=keyboards.result_menu())

        # ─── مرحله ۵: ارسال فایل ───
        with open(output_path, "rb") as f:
            await q.message.reply_document(
                document=f,
                filename=output_path.name,
                caption=cards.result_caption(result["compressed_size"], result["ratio"]),
                parse_mode=ParseMode.HTML,
            )

        # ─── آمار ───
        _update_stats(ctx, result, mime)

    except Exception as e:
        log_msg = str(e)[:120]
        await edit_func(cards.error_card(log_msg, "دوباره تلاش کن یا سطح دیگه انتخاب کن"))

    finally:
        # پاک‌سازی
        try: input_path.unlink(missing_ok=True)
        except: pass
        try:
            if output_path and output_path.exists():
                output_path.unlink(missing_ok=True)
        except: pass


def _update_stats(ctx, result: dict, mime: str):
    """به‌روزرسانی فایل آمار"""
    stats = load_json(STATS_FILE, {
        "videos": 0, "images": 0, "audios": 0,
        "pdfs": 0, "files": 0, "total_saved": 0,
    })
    saved = result["original_size"] - result["compressed_size"]
    stats["total_saved"] = stats.get("total_saved", 0) + max(0, saved)

    if mime.startswith("video/"):       stats["videos"] = stats.get("videos", 0) + 1
    elif mime.startswith("image/"):     stats["images"] = stats.get("images", 0) + 1
    elif mime.startswith("audio/"):     stats["audios"] = stats.get("audios", 0) + 1
    elif mime == "application/pdf":     stats["pdfs"]   = stats.get("pdfs", 0) + 1
    else:                                stats["files"]  = stats.get("files", 0) + 1

    save_json(STATS_FILE, stats)

    # ─── کاربر ───
    user_id = str(ctx._user_id) if hasattr(ctx, "_user_id") else None
    # (این خط رو می‌شه با user_id از update گرفت)
