"""
⚡ HiVo Compressor — Main entry
اجرا روی GitHub Actions با self-restart
"""
import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters,
)

from config import BOT_TOKEN, ADMIN_ID, SUPPORT_USER
from core.system import get_system_info
from handlers import start as h_start
from handlers import receive as h_receive
from handlers import compress as h_compress
from handlers import stats as h_stats
from handlers import help as h_help
from handlers import misc as h_misc


logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)
log = logging.getLogger("HiVo")


def main():
    if not BOT_TOKEN:
        raise SystemExit("❌ BOT_TOKEN تنظیم نشده!")

    info = get_system_info()
    log.info(f"⚡ HiVo Compressor booting...")
    log.info(f"🔧 Cores: {info['cores']}  |  Encoder: {info['encoder']}")

    app = Application.builder().token(BOT_TOKEN).build()

    # ─── Commands ───
    app.add_handler(CommandHandler("start", h_start.cmd_start))
    app.add_handler(CommandHandler("help",  h_help.cb_help))

    # ─── Files ───
    app.add_handler(MessageHandler(
        filters.VIDEO | filters.Document.ALL | filters.AUDIO
        | filters.PHOTO | filters.VOICE,
        h_receive.cmd_receive,
    ))

    # ─── Callbacks ───
    app.add_handler(CallbackQueryHandler(h_compress.cb_quality, pattern=r"^q:"))
    app.add_handler(CallbackQueryHandler(h_stats.cb_stats,     pattern=r"^stats$"))
    app.add_handler(CallbackQueryHandler(h_help.cb_help,       pattern=r"^help$"))
    app.add_handler(CallbackQueryHandler(h_misc.cb_back,       pattern=r"^back$"))
    app.add_handler(CallbackQueryHandler(h_misc.cb_cancel,     pattern=r"^cancel$"))

    log.info("🚀 Bot is polling...")
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES,
    )


if __name__ == "__main__":
    main()
