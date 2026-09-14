"""
🖼️ موتور فشرده‌سازی عکس
WebP + Pillow (بهترین نسبت حجم/کیفیت)
"""
import asyncio
from pathlib import Path
from PIL import Image


class ImageCompressor:
    QUALITY = {"fast": 70, "balanced": 82, "max": 92}

    @classmethod
    async def compress(cls, input_path: Path, output_path: Path,
                       mode: str = "balanced", progress_cb=None) -> dict:
        q = cls.QUALITY.get(mode, 82)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, cls._sync_compress, input_path, output_path, q)

        original   = input_path.stat().st_size
        compressed = output_path.stat().st_size

        return {
            "original_size":   original,
            "compressed_size": compressed,
            "ratio":           round((1 - compressed / original) * 100, 1),
            "encoder":         "WebP",
        }

    @staticmethod
    def _sync_compress(inp: Path, out: Path, quality: int):
        img = Image.open(inp)
        # تبدیل مد
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")
        elif img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        # resize اگه خیلی بزرگه (بیشتر از 4K)
        MAX_DIM = 3840
        if max(img.size) > MAX_DIM:
            img.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)

        img.save(out, "WEBP", quality=quality, method=6, optimize=True)
