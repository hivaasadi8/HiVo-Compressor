"""
📕 موتور فشرده‌سازی PDF با Ghostscript
"""
import asyncio
from pathlib import Path


class PDFCompressor:
    # سطوح Ghostscript
    PRESETS = {
        "fast":     "/screen",    # 72 dpi — کم‌ترین حجم
        "balanced": "/ebook",     # 150 dpi — پیشنهاد
        "max":      "/printer",   # 300 dpi — چاپ
    }

    @classmethod
    async def compress(cls, input_path: Path, output_path: Path,
                       mode: str = "balanced", progress_cb=None) -> dict:
        preset = cls.PRESETS.get(mode, "/ebook")

        cmd = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.5",
            f"-dPDFSETTINGS={preset}",
            "-dNOPAUSE", "-dQUIET", "-dBATCH",
            "-dDetectDuplicateImages=true",
            "-dCompressFonts=true",
            "-dSubsetFonts=true",
            "-dEmbedAllFonts=true",
            f"-sOutputFile={output_path}",
            str(input_path),
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.wait()

        original   = input_path.stat().st_size
        compressed = output_path.stat().st_size

        return {
            "original_size":   original,
            "compressed_size": compressed,
            "ratio":           round((1 - compressed / original) * 100, 1),
            "encoder":         "Ghostscript",
        }
