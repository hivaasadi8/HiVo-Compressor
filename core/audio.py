"""
🎵 موتور فشرده‌سازی صدا
"""
import asyncio
from pathlib import Path


class AudioCompressor:
    PRESETS = {
        "fast":     {"codec": "libopus",  "bitrate": "64k",  "hz": "24000"},
        "balanced": {"codec": "libopus",  "bitrate": "96k",  "hz": "48000"},
        "max":      {"codec": "libopus",  "bitrate": "160k", "hz": "48000"},
    }

    @classmethod
    async def compress(cls, input_path: Path, output_path: Path,
                       mode: str = "balanced", progress_cb=None) -> dict:
        cfg = cls.PRESETS.get(mode, cls.PRESETS["balanced"])

        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(input_path),
            "-c:a", cfg["codec"],
            "-b:a", cfg["bitrate"],
            "-ar", cfg["hz"],
            "-ac", "2",
            "-progress", "pipe:1", "-nostats",
            str(output_path),
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()

        original   = input_path.stat().st_size
        compressed = output_path.stat().st_size

        return {
            "original_size":   original,
            "compressed_size": compressed,
            "ratio":           round((1 - compressed / original) * 100, 1),
            "encoder":         cfg["codec"],
        }
