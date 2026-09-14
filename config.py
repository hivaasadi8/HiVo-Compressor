"""
⚡ HiVo Compressor — Central Configuration
"""
import os
from pathlib import Path

# ─── توکن‌ها و اعتبارسنجی ───
BOT_TOKEN       = os.getenv("BOT_TOKEN", "")
ADMIN_ID        = int(os.getenv("ADMIN_ID", "0"))
GITHUB_TOKEN    = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO     = os.getenv("GITHUB_REPO", "")
GITHUB_RUN_ID   = os.getenv("GITHUB_RUN_ID", "")
SUPPORT_USER    = os.getenv("SUPPORT_USER", "HiVoSupport")

# ─── مسیرها ───
BASE_DIR  = Path(__file__).parent.resolve()
DATA_DIR  = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
TEMP_DIR  = Path(os.getenv("TEMP_DIR", "/tmp/hivo"))

for d in (DATA_DIR, TEMP_DIR, ASSETS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ─── فایل‌های داده ───
USERS_FILE    = DATA_DIR / "users.json"
STATS_FILE    = DATA_DIR / "stats.json"
SETTINGS_FILE = DATA_DIR / "settings.json"

# ─── محدودیت‌ها ───
MAX_FILE_SIZE_MB   = 1900              # زیر سقف 2GB تلگرام
MAX_CONCURRENT     = 2                 # حداکثر فشرده‌سازی همزمان
RATE_LIMIT_SECONDS = 30                # فاصله بین درخواست‌ها
MAX_DAILY_PER_USER = 30                # حداکثر فایل در روز

# ─── انکودرها ───
VIDEO_ENCODERS = ["libx264", "libx265", "libvpx-vp9"]
AUDIO_CODECS   = ["aac", "libopus", "libmp3lame"]
IMAGE_FORMATS  = ["WEBP", "JPEG", "PNG"]

# ─── اجرا ───
if not BOT_TOKEN:
    raise SystemExit("❌ BOT_TOKEN تنظیم نشده است!")
