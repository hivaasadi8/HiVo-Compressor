"""
🧠 ارکستراتور اصلی — انتخاب موتور مناسب
"""
from pathlib import Path

from .detector  import detect_file_type
from .video     import VideoCompressor
from .audio     import AudioCompressor
from .image     import ImageCompressor
from .pdf       import PDFCompressor
from .archive   import ArchiveCompressor


class UniversalCompressor:

    @classmethod
    async def compress(cls, input_path: Path, mode: str = "balanced", progress_cb=None):
        info = detect_file_type(input_path)
        cat = info["category"]

        # ─── ویدئو ───
        if cat == "video":
            out = input_path.with_name(f"HiVo_{input_path.stem}.mp4")
            result = await VideoCompressor.compress(input_path, out, mode, progress_cb)

        # ─── گیف (به mp4 تبدیل می‌کنیم که حجمش نصف بشه) ───
        elif cat == "gif":
            out = input_path.with_name(f"HiVo_{input_path.stem}.mp4")
            result = await VideoCompressor.compress(input_path, out, mode, progress_cb)

        # ─── عکس ───
        elif cat == "image":
            out = input_path.with_suffix(".webp")
            result = await ImageCompressor.compress(input_path, out, mode, progress_cb)

        # ─── صدا ───
        elif cat == "audio":
            out = input_path.with_suffix(".opus")
            result = await AudioCompressor.compress(input_path, out, mode, progress_cb)

        # ─── PDF ───
        elif cat == "pdf":
            out = input_path.with_name(f"HiVo_{input_path.name}")
            result = await PDFCompressor.compress(input_path, out, mode, progress_cb)

        # ─── آرشیو ───
        elif cat == "archive":
            out = Path(str(input_path) + ".zst")
            result = await ArchiveCompressor.compress(input_path, out, mode, progress_cb)

        # ─── ناشناخته → Zstd ───
        else:
            out = Path(str(input_path) + ".zst")
            result = await ArchiveCompressor.compress(input_path, out, mode, progress_cb)

        # اگه فشرده‌سازی نتیجه نداشت (بزرگ‌تر شد)، فایل اصلی رو برگردون
        if result["compressed_size"] >= result["original_size"]:
            result["compressed_size"] = result["original_size"]
            result["ratio"] = 0.0
            result["encoder"] += " (no gain)"

        return result, out
