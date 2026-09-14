"""
⚡ تشخیص نوع فایل — MIME + Extension + Magic Bytes
"""
import mimetypes
from pathlib import Path


def detect_file_type(path: Path) -> dict:
    """تشخیص کامل نوع فایل"""
    mime, _ = mimetypes.guess_type(str(path))
    ext = path.suffix.lower()
    size = path.stat().st_size

    # Magic bytes (برای دقت بالاتر)
    try:
        with open(path, "rb") as f:
            header = f.read(16)
    except Exception:
        header = b""

    category = "unknown"
    subtype = ext.lstrip(".")

    # ─── ویدئو ───
    video_exts = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".mpg", ".mpeg", ".3gp"}
    if ext in video_exts or (mime and mime.startswith("video/")):
        category = "video"

    # ─── عکس ───
    image_exts = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".gif", ".webp", ".heic", ".avif"}
    if ext in image_exts or (mime and mime.startswith("image/")):
        # GIF رو جدا می‌کنیم چون انیمیشن داره
        if ext == ".gif":
            category = "gif"
        else:
            category = "image"

    # ─── صدا ───
    audio_exts = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".opus", ".m4a", ".wma", ".aiff"}
    if ext in audio_exts or (mime and mime.startswith("audio/")):
        category = "audio"

    # ─── PDF ───
    if ext == ".pdf" or header.startswith(b"%PDF"):
        category = "pdf"

    # ─── آرشیو ───
    archive_exts = {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".zst"}
    if ext in archive_exts:
        category = "archive"

    return {
        "category": category,
        "mime":     mime or "application/octet-stream",
        "ext":      ext,
        "size":     size,
        "subtype":  subtype,
    }


def get_file_emoji(category: str) -> str:
    return {
        "video":   "🎬",
        "image":   "🖼️",
        "gif":     "🎞️",
        "audio":   "🎵",
        "pdf":     "📕",
        "archive": "📦",
        "unknown": "📄",
    }.get(category, "📄")


def get_human_category(category: str) -> str:
    return {
        "video":   "ویدئو",
        "image":   "تصویر",
        "gif":     "گیف",
        "audio":   "صدا",
        "pdf":     "سند PDF",
        "archive": "آرشیو",
        "unknown": "فایل",
    }.get(category, "فایل")
